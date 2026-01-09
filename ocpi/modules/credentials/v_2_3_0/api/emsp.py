import httpx
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
)
from fastapi import (
    status as fastapistatus,
)

from ocpi.core import status
from ocpi.core.adapter import Adapter
from ocpi.core.authentication.verifier import (
    AuthorizationVerifier,
    CredentialsAuthorizationVerifier,
)
from ocpi.core.config import logger
from ocpi.core.crud import Crud
from ocpi.core.dependencies import get_adapter, get_crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.schemas import OCPIResponse
from ocpi.core.utils import encode_string_base64, get_auth_token
from ocpi.modules.credentials.v_2_3_0.schemas import Credentials
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/credentials",
)
cred_dependency = CredentialsAuthorizationVerifier(VersionNumber.v_2_3_0)


@router.get(
    "/",
    response_model=OCPIResponse,
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)
async def get_credentials(
    request: Request,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get credentials.

    Retrieves credentials based on the specified parameters.

    **Returns:**
        The OCPIResponse containing the credentials.
    """
    logger.info("Received request to get credentials")
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.credentials_and_registration,
        RoleEnum.emsp,
        auth_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    return OCPIResponse(
        data=adapter.credentials_adapter(data, VersionNumber.v_2_3_0).model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("/", response_model=OCPIResponse)
async def post_credentials(
    request: Request,
    credentials: Credentials,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    """
    Create credentials.

    Creates credentials based on the specified parameters.

    **Request body:**
        credentials (Credentials): The credentials object.

    **Returns:**
        The OCPIResponse containing the new credentials.

    **Raises:**
        HTTPException: If the client is already registered
            (HTTP 405 Method Not Allowed)
                       or if the token is not valid (HTTP 401 Unauthorized).
    """
    logger.info("Received request to create credentials.")
    logger.debug(f"POST credentials body: {credentials.model_dump()}")

    auth_token = get_auth_token(request)

    # Check if the client is already registered
    if server_cred:
        logger.info("Client already registered.")

        raise HTTPException(
            fastapistatus.HTTP_405_METHOD_NOT_ALLOWED,
            "Client is already registered",
        )
    if server_cred is None:
        logger.info("Token is not valid.")

        raise HTTPException(
            fastapistatus.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
        )

    # Retrieve the versions and endpoints from the client
    async with httpx.AsyncClient() as client:
        credentials_client_token = credentials.token
        authorization_token = f"Token {encode_string_base64(credentials_client_token)}"

        logger.info(f"Send request to get versions: {credentials.url}")

        response_versions = await client.get(
            credentials.url, headers={"authorization": authorization_token}
        )

        logger.info(f"GET versions status_code: {response_versions.status_code}")

        if response_versions.status_code == fastapistatus.HTTP_200_OK:
            version_url = None
            versions = response_versions.json()["data"]

            logger.debug(f"GET versions response data: {versions}")

            for version in versions:
                if version["version"] == VersionNumber.v_2_3_0:
                    version_url = version["url"]

            if not version_url:
                logger.debug(f"Version {VersionNumber.v_2_3_0} is not supported")

                return OCPIResponse(
                    data=[],
                    **status.OCPI_3002_UNSUPPORTED_VERSION,
                )

            logger.info(f"Send request to get version details: {version_url}")

            response_endpoints = await client.get(
                version_url, headers={"authorization": authorization_token}
            )

            logger.info(
                f"GET version details status_code: {response_endpoints.status_code}"
            )

            if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
                # Store client credentials and generate new credentials for sender
                endpoints = response_endpoints.json()["data"]

                logger.debug(f"GET version details response data: {endpoints}")

                new_credentials = await crud.create(
                    ModuleID.credentials_and_registration,
                    RoleEnum.emsp,
                    {"credentials": credentials.model_dump(), "endpoints": endpoints},
                    auth_token=auth_token,
                    version=VersionNumber.v_2_3_0,
                )

                return OCPIResponse(
                    data=adapter.credentials_adapter(
                        new_credentials, VersionNumber.v_2_3_0
                    ).model_dump(),
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )

    return OCPIResponse(
        data=[],
        **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
    )


@router.put("/", response_model=OCPIResponse)
async def update_credentials(
    request: Request,
    credentials: Credentials,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    """
    Update credentials.

    Updates credentials based on the specified parameters.

    **Request body:**
        credentials (Credentials): The credentials object.

    **Returns:**
        The OCPIResponse containing the updated credentials.

    **Raises:**
        HTTPException: If the client is not registered
            (HTTP 405 Method Not Allowed).
    """
    logger.info("Received request to update credentials.")
    logger.debug(f"PUT credentials body: {credentials.model_dump()}")
    auth_token = get_auth_token(request)

    # Check if the client is already registered
    if not server_cred:
        logger.info("Client already registered.")

        raise HTTPException(
            fastapistatus.HTTP_405_METHOD_NOT_ALLOWED,
            "Client is not registered",
        )

    # Retrieve the versions and endpoints from the client
    async with httpx.AsyncClient() as client:
        credentials_client_token = credentials.token
        authorization_token = f"Token {encode_string_base64(credentials_client_token)}"

        logger.info(f"Send request to get versions: {credentials.url}")

        response_versions = await client.get(
            credentials.url, headers={"authorization": authorization_token}
        )

        logger.info(f"GET versions status_code: {response_versions.status_code}")

        if response_versions.status_code == fastapistatus.HTTP_200_OK:
            version_url = None
            versions = response_versions.json()["data"]

            logger.debug(f"GET versions response data: {versions}")

            for version in versions:
                if version["version"] == VersionNumber.v_2_3_0:
                    version_url = version["url"]

            if not version_url:
                logger.debug(f"Version {VersionNumber.v_2_3_0} is not supported")

                return OCPIResponse(
                    data=[],
                    **status.OCPI_3002_UNSUPPORTED_VERSION,
                )

            logger.info(f"Send request to get version details: {version_url}")

            response_endpoints = await client.get(
                version_url, headers={"authorization": authorization_token}
            )

            logger.info(
                f"GET version details status_code: {response_endpoints.status_code}"
            )

            if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
                # Update server credentials to access client's
                # system and generate new credentials token
                endpoints = response_endpoints.json()["data"]

                logger.debug(f"GET version details response data: {endpoints}")

                new_credentials = await crud.update(
                    ModuleID.credentials_and_registration,
                    RoleEnum.emsp,
                    {"credentials": credentials.model_dump(), "endpoints": endpoints},
                    # TODO check credential_id
                    id="",
                    auth_token=auth_token,
                    version=VersionNumber.v_2_3_0,
                )

                return OCPIResponse(
                    data=adapter.credentials_adapter(
                        new_credentials, VersionNumber.v_2_3_0
                    ).model_dump(),
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )

    return OCPIResponse(
        data=[],
        **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
    )


@router.delete(
    "/",
    response_model=OCPIResponse,
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)
async def remove_credentials(
    request: Request,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Remove credentials.

    Deletes credentials based on the specified parameters.

    **Returns:**
        The OCPIResponse indicating the successful removal of credentials.

    **Raises:**
        HTTPException: If the client is not registered
            (HTTP 405 Method Not Allowed).
    """
    logger.info("Received request to delete credentials")

    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.credentials_and_registration,
        RoleEnum.emsp,
        auth_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    if not data:
        raise HTTPException(
            fastapistatus.HTTP_405_METHOD_NOT_ALLOWED,
            "Client is not registered",
        )

    await crud.delete(
        ModuleID.credentials_and_registration,
        RoleEnum.emsp,
        auth_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
