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
from ocpi.core.authentication.verifier import (
    VersionsAuthorizationVerifier,
)
from ocpi.core.config import logger
from ocpi.core.crud import Crud
from ocpi.core.dependencies import get_crud, get_endpoints
from ocpi.core.schemas import OCPIResponse
from ocpi.modules.versions.v_2_3_0.schemas import (
    VersionDetail,
    VersionNumber,
)

router = APIRouter()
cred_dependency = VersionsAuthorizationVerifier(VersionNumber.v_2_3_0)


@router.get("/2.3.0/details", response_model=OCPIResponse)
async def get_version_details(
    request: Request,
    endpoints=Depends(get_endpoints),
    crud: Crud = Depends(get_crud),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    """
    Get Version Details.

    Retrieves details of the OCPI version 2.3.0.

    **Returns:**
        The OCPIResponse containing details of the OCPI version 2.3.0.
    """
    logger.info(f"Received request for version details: {request.url}")
    if server_cred is None:
        logger.debug("Unauthorized request.")
        raise HTTPException(fastapistatus.HTTP_401_UNAUTHORIZED, "Unauthorized")

    return OCPIResponse(
        data=VersionDetail(
            version=VersionNumber.v_2_3_0,
            endpoints=endpoints[VersionNumber.v_2_3_0],
        ).model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
