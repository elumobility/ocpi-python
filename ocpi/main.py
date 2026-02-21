from typing import Any
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi import status as fastapistatus
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)

from ocpi.core import status
from ocpi.core.adapter import BaseAdapter
from ocpi.core.config import logger, settings
from ocpi.core.data_types import URL
from ocpi.core.dependencies import (
    get_adapter,
    get_authenticator,
    get_crud,
    get_endpoints,
    get_modules,
    get_versions,
)
from ocpi.core.endpoints import ENDPOINTS
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError
from ocpi.core.push import (
    http_router as http_push_router,
)
from ocpi.core.push import (
    websocket_router as websocket_push_router,
)
from ocpi.core.routers import ROUTERS
from ocpi.core.schemas import OCPIResponse
from ocpi.modules.versions import router as versions_router
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.schemas import Version


class HubRequestIdMiddleware(BaseHTTPMiddleware):
    """Echo X-Request-ID and X-Correlation-ID headers per the OCPI spec.

    Every request receives a unique X-Request-ID in the response.
    If the client provides X-Correlation-ID it is echoed back unchanged.
    """

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        correlation_id = request.headers.get("X-Correlation-ID")

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        if correlation_id:
            response.headers["X-Correlation-ID"] = correlation_id
        return response


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        logger.debug(f"{request.method}: {request.url}")
        logger.debug(f"Request headers - {request.headers}")

        try:
            response = await call_next(request)
        except AuthorizationOCPIError as e:
            logger.warning("OCPI middleware AuthorizationOCPIError exception.")
            response = JSONResponse(
                content={"detail": str(e)},
                status_code=fastapistatus.HTTP_403_FORBIDDEN,
            )
        except NotFoundOCPIError as e:
            logger.warning("OCPI middleware NotFoundOCPIError exception.")
            response = JSONResponse(
                content={"detail": str(e)},
                status_code=fastapistatus.HTTP_404_NOT_FOUND,
            )
        except ValidationError as e:
            logger.warning("OCPI middleware ValidationError exception.")
            logger.error(f"ValidationError details: {str(e)}")
            import traceback

            logger.error(f"ValidationError traceback: {traceback.format_exc()}")
            response = JSONResponse(
                OCPIResponse(
                    data=[],
                    **status.OCPI_3000_GENERIC_SERVER_ERROR,
                ).model_dump()
            )
        except Exception as e:
            logger.warning(f"Unknown exception: {str(e)}.")
            response = JSONResponse(
                OCPIResponse(
                    data=[],
                    **status.OCPI_3000_GENERIC_SERVER_ERROR,
                ).model_dump()
            )

        logger.debug(f"Response status_code -> {response.status_code}.")
        return response


def get_application(
    version_numbers: list[VersionNumber],
    roles: list[RoleEnum],
    crud: Any,
    modules: list[ModuleID],
    authenticator: Any,
    adapter: Any = BaseAdapter,
    http_push: bool = False,
    websocket_push: bool = False,
) -> FastAPI:
    """
    Create and configure an OCPI FastAPI application.

    This is the main entry point for creating an OCPI-compliant API server.
    The function sets up all necessary routes, middleware, and authentication
    based on the provided configuration.

    Args:
        version_numbers: List of OCPI versions to support (e.g., [VersionNumber.v_2_3_0]).
            Supported versions: 2.3.0, 2.2.1, 2.1.1
        roles: List of OCPI roles to enable (e.g., [RoleEnum.cpo, RoleEnum.emsp]).
            Available roles: CPO (Charge Point Operator), EMSP (eMobility Service Provider),
            PTP (Payment Terminal Provider)
        crud: CRUD class implementing business logic and data operations.
            Must implement async methods: list(), get(), create(), update(), delete()
        modules: List of OCPI modules to enable (e.g., [ModuleID.locations, ModuleID.sessions]).
            Available modules: locations, sessions, cdrs, tokens, tariffs, commands,
            chargingprofiles, hubclientinfo, credentials, payments
        authenticator: Authenticator class for token validation.
            Must implement: get_valid_token_c() and get_valid_token_a()
        adapter: Optional adapter class for data transformation (default: BaseAdapter).
        http_push: If True, enables HTTP push endpoints for sending commands to clients.
        websocket_push: If True, enables WebSocket endpoints for real-time data updates.

    Returns:
        FastAPI: Configured FastAPI application instance ready to run with uvicorn.

    Example:
        ```python
        from ocpi import get_application
        from ocpi.core.enums import RoleEnum, ModuleID
        from ocpi.modules.versions.enums import VersionNumber
        from myapp.auth import MyAuthenticator
        from myapp.crud import MyCrud

        # Create OCPI application
        app = get_application(
            version_numbers=[VersionNumber.v_2_3_0],
            roles=[RoleEnum.cpo],
            modules=[ModuleID.locations, ModuleID.sessions],
            authenticator=MyAuthenticator,
            crud=MyCrud,
        )

        # Run with: uvicorn main:app --reload
        ```

    Note:
        - All CRUD methods must be async
        - Authentication tokens must be validated according to OCPI version
          (2.2.1 and 2.3.0 require Base64-encoded tokens)
        - Some modules are related (e.g., sessions require locations)
        - See examples/ directory for complete working examples
    """
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"/{settings.OCPI_PREFIX}/docs",
        redoc_url=f"/{settings.OCPI_PREFIX}/redoc",
        openapi_url=f"/{settings.OCPI_PREFIX}/openapi.json",
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(ExceptionHandlerMiddleware)
    _app.add_middleware(HubRequestIdMiddleware)

    _app.include_router(
        versions_router,
        prefix=f"/{settings.OCPI_PREFIX}",
    )

    if http_push:
        _app.include_router(
            http_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    if websocket_push:
        _app.include_router(
            websocket_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    versions = []
    version_endpoints: dict[str, list] = {}

    for version in version_numbers:
        mapped_version = ROUTERS.get(version)
        if not mapped_version:
            raise ValueError("Version isn't supported yet.")

        _app.include_router(
            mapped_version["version_router"],  # type: ignore[arg-type]
            prefix=f"/{settings.OCPI_PREFIX}",
        )

        versions.append(
            Version(
                version=version,
                url=URL(
                    f"{settings.PROTOCOL}://{settings.OCPI_HOST}/"
                    f"{settings.OCPI_PREFIX}/{version.value}/details"
                ),
            ).model_dump(),
        )

        version_endpoints[version] = []

        if RoleEnum.cpo in roles:
            for module in modules:
                cpo_router = mapped_version["cpo_router"].get(module)  # type: ignore[attr-defined]
                if cpo_router:
                    _app.include_router(
                        cpo_router,  # type: ignore[arg-type]
                        prefix=f"/{settings.OCPI_PREFIX}/cpo/{version.value}",
                        tags=[f"CPO {version.value}"],
                    )
                    endpoint = ENDPOINTS[version][RoleEnum.cpo].get(module)  # type: ignore[index]
                    if endpoint:
                        version_endpoints[version].append(endpoint)

        if RoleEnum.emsp in roles:
            for module in modules:
                emsp_router = mapped_version["emsp_router"].get(module)  # type: ignore[attr-defined]
                if emsp_router:
                    _app.include_router(
                        emsp_router,  # type: ignore[arg-type]
                        prefix=f"/{settings.OCPI_PREFIX}/emsp/{version.value}",
                        tags=[f"EMSP {version.value}"],
                    )
                    endpoint = ENDPOINTS[version][RoleEnum.emsp].get(module)  # type: ignore[index]
                    if endpoint:
                        version_endpoints[version].append(endpoint)

        if RoleEnum.ptp in roles:
            for module in modules:
                ptp_router = mapped_version.get("ptp_router", {}).get(module)  # type: ignore[attr-defined]
                if ptp_router:
                    _app.include_router(
                        ptp_router,  # type: ignore[arg-type]
                        prefix=f"/{settings.OCPI_PREFIX}/ptp/{version.value}",
                        tags=[f"PTP {version.value}"],
                    )

    def override_get_crud():
        return crud

    _app.dependency_overrides[get_crud] = override_get_crud

    def override_get_adapter():
        return adapter

    _app.dependency_overrides[get_adapter] = override_get_adapter

    def override_get_versions():
        return versions

    _app.dependency_overrides[get_versions] = override_get_versions

    def override_get_endpoints():
        return version_endpoints

    _app.dependency_overrides[get_endpoints] = override_get_endpoints

    def override_get_modules():
        return modules

    _app.dependency_overrides[get_modules] = override_get_modules

    def override_get_authenticator():
        return authenticator

    _app.dependency_overrides[get_authenticator] = override_get_authenticator

    return _app
