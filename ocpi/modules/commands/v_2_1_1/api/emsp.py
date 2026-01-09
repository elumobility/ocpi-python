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
from ocpi.modules.commands.v_2_1_1.schemas import CommandResponse
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/commands",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.post("/{uid}", response_model=OCPIResponse)
async def receive_command_result(
    request: Request,
    uid: str,
    command_response: CommandResponse,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Receive Command Result.

    Processes and handles incoming command results.

    **Path parameters:**
        - uid (str): The unique identifier associated with the command.

    **Request body:**
        command_response (CommandResponse): The response data associated
            with the command.

    **Returns:**
        The OCPIResponse indicating the success or failure of processing
            the command result.
    """
    logger.info(f"Received command result with uid - `{uid}`.")
    logger.debug(f"Command response data - {command_response.model_dump()}")
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    await crud.update(
        ModuleID.commands,
        RoleEnum.emsp,
        command_response.model_dump(),
        uid,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
