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
    prefix="/sessions",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.get("/", response_model=OCPIResponse)
async def get_sessions(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get sessions.

    Retrieves a list of sessions based on the specified filters.

    **Query parameters:**
        - limit (int): Maximum number of objects to GET (default=50).
        - offset (int): The offset of the first object returned (default=0).
        - date_from (datetime): Only return Sessions that have last_updated
            after this Date/Time (default=None).
        - date_to (datetime): Only return Sessions that have last_updated
            before this Date/Time (default=None).

    **Returns:**
        The OCPIResponse containing the list of CDRs.
    """
    logger.info("Received request to get sessions.")
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data_list = await get_list(
        response,
        filters,
        ModuleID.sessions,
        RoleEnum.cpo,
        VersionNumber.v_2_1_1,
        crud,
        auth_token=auth_token,
    )

    sessions = []
    for data in data_list:
        sessions.append(
            adapter.session_adapter(data, VersionNumber.v_2_1_1).model_dump()
        )
    logger.debug(f"Amount of sessions in response: {len(sessions)}")
    return OCPIResponse(
        data=sessions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
