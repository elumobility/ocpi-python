from fastapi import APIRouter, Depends, Request, Response

from ocpi.core import status
from ocpi.core.adapter import Adapter
from ocpi.core.authentication.verifier import AuthorizationVerifier
from ocpi.core.config import logger
from ocpi.core.crud import Crud
from ocpi.core.data_types import CiString
from ocpi.core.dependencies import get_adapter, get_crud, pagination_filters
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.schemas import OCPIResponse
from ocpi.core.utils import get_auth_token, get_list
from ocpi.modules.sessions.v_2_3_0.schemas import ChargingPreferences
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/sessions",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
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
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.sessions,
        RoleEnum.cpo,
        VersionNumber.v_2_3_0,
        crud,
        auth_token=auth_token,
    )

    sessions = []
    for data in data_list:
        sessions.append(
            adapter.session_adapter(data, VersionNumber.v_2_3_0).model_dump()
        )
    logger.debug(f"Amount of sessions in response: {len(sessions)}")
    return OCPIResponse(
        data=sessions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put("/{session_id}/charging_preferences", response_model=OCPIResponse)
async def set_charging_preference(
    request: Request,
    session_id: CiString(36),  # type: ignore
    charging_preferences: ChargingPreferences,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Set Charging Preference.

    Updates the charging preference for a specific charging session.

    **Path parameters:**
        - session_id (str): The ID of the charging session (36 characters).

    **Request body:**
        charging_preferences (ChargingPreferences): The charging preferences
            object.

    **Returns:**
        The OCPIResponse containing the updated charging preferences.
    """
    auth_token = get_auth_token(request)
    data = await crud.update(
        ModuleID.sessions,
        RoleEnum.cpo,
        charging_preferences.model_dump(),
        session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    return OCPIResponse(
        data=[adapter.charging_preference_adapter(data).model_dump()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
