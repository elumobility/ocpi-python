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
from ocpi.core.dependencies import (
    get_crud,
)
from ocpi.core.dependencies import (
    get_versions as get_versions_,
)
from ocpi.core.schemas import OCPIResponse

router = APIRouter()
cred_dependency = VersionsAuthorizationVerifier(None)


@router.get("/versions", response_model=OCPIResponse)
async def get_versions(
    request: Request,
    versions=Depends(get_versions_),
    crud: Crud = Depends(get_crud),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    """
    Get OCPI Versions.

    Retrieves a list of available OCPI versions.

    **Returns:**
        The OCPIResponse containing a list of available OCPI versions.
    """
    logger.info(f"Received request for version details: {request.url}")
    if server_cred is None:
        logger.debug("Unauthorized request.")
        raise HTTPException(
            fastapistatus.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
        )
    return OCPIResponse(
        data=versions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
