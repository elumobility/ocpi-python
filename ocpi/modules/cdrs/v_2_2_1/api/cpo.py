from fastapi import APIRouter, Depends, Request, Response

from ocpi.core import status
from ocpi.core.adapter import Adapter
from ocpi.core.authentication.verifier import AuthorizationVerifier
from ocpi.core.config import logger
from ocpi.core.crud import Crud
from ocpi.core.dependencies import get_adapter, get_crud, pagination_filters
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.schemas import OCPIResponse
from ocpi.core.utils import get_auth_token, get_list
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/cdrs",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get("/", response_model=OCPIResponse)
async def get_cdrs(
    response: Response,
    request: Request,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get CDRs.

    Retrieves a list of Charge Detail Records (CDRs) based
     on the specified filters.

    **Query parameters:**
        - limit (int): Maximum number of objects to GET (default=50).
        - offset (int): The offset of the first object returned (default=0).
        - date_from (datetime): Only return Locations that have last_updated
            after this Date/Time (default=None).
        - date_to (datetime): Only return Locations that have last_updated
            before this Date/Time (default=None).

    **Returns:**
        The OCPIResponse containing the list of CDRs.
    """
    logger.info("Received request to get cdrs.")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.cdrs,
        RoleEnum.cpo,
        VersionNumber.v_2_2_1,
        crud,
        auth_token=auth_token,
    )

    cdrs = []
    for data in data_list:
        cdrs.append(adapter.cdr_adapter(data).model_dump())
    logger.debug(f"Amount of cdrs in response: {len(cdrs)}")
    return OCPIResponse(
        data=cdrs,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
