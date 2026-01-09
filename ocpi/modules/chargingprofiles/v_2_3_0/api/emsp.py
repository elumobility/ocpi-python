from fastapi import APIRouter, Depends, Request

from ocpi.core import status
from ocpi.core.adapter import Adapter
from ocpi.core.authentication.verifier import AuthorizationVerifier
from ocpi.core.config import logger
from ocpi.core.crud import Crud
from ocpi.core.dependencies import get_adapter, get_crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.schemas import OCPIResponse
from ocpi.core.utils import get_auth_token
from ocpi.modules.chargingprofiles.v_2_3_0.schemas import (
    ActiveChargingProfile,
)
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/chargingprofiles",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)


@router.post("/", response_model=OCPIResponse)
async def receive_chargingprofile_command(
    request: Request,
    data: dict,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Receive Charging Profile Command.

    Receives and processes the charging profile command.

    **Parameters:**
        - data (dict): The charging profile command data.

    **Returns:**
        The OCPIResponse indicating the success of the operation.
    """
    logger.info("Received charging profile result.")
    logger.debug(f"Chargingprofile result data - {data}")
    auth_token = get_auth_token(request)
    query_params = request.query_params
    logger.debug(f"Request query_params - {query_params}")

    await crud.create(
        ModuleID.charging_profile,
        RoleEnum.emsp,
        data,
        query_params=query_params,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put("/{session_id}", response_model=OCPIResponse)
async def add_or_update_chargingprofile(
    request: Request,
    session_id: str,
    active_charging_profile: ActiveChargingProfile,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Charging Profile.

    Adds or updates the active charging profile for a specific session.

    **Parameters:**
        - session_id (str): The ID of the charging session.

    **Request body:**
        - active_charging_profile (ActiveChargingProfile): The data
            of the active charging profile.

    **Returns:**
        The OCPIResponse indicating the success of the operation.
    """
    logger.info(
        "Received request to add or update charging profile "
        f"with session_id - `{session_id}`."
    )
    logger.debug(
        f"Active chargingprofile result data - {active_charging_profile.model_dump()}"
    )
    auth_token = get_auth_token(request)

    await crud.update(
        ModuleID.charging_profile,
        RoleEnum.emsp,
        active_charging_profile.model_dump(),
        0,
        session_id=session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
