from fastapi import APIRouter, Depends, Request

from py_ocpi.core import status
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.config import logger
from py_ocpi.core.crud import Crud
from py_ocpi.core.dependencies import get_adapter, get_crud
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import get_auth_token
from py_ocpi.modules.commands.v_2_3_0.schemas import CommandResult
from py_ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/commands",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)


@router.post("/{uid}", response_model=OCPIResponse)
async def receive_command_result(
    request: Request,
    uid: str,
    command_result: CommandResult,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Receive Command Result.

    Processes and handles incoming command results.

    **Path parameters:**
        - uid (str): The unique identifier associated with the command.

    **Request body:**
        command_response (CommandResponse): The response data
            associated with the command.

    **Returns:**
        The OCPIResponse indicating the success or failure of
            processing the command result.
    """
    logger.info(f"Received command result with uid - `{uid}`.")
    logger.debug(f"Command result data - {command_result.model_dump()}")
    auth_token = get_auth_token(request)

    await crud.update(
        ModuleID.commands,
        RoleEnum.emsp,
        command_result.model_dump(),
        uid,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
