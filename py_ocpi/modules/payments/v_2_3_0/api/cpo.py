"""CPO API for payments module - OCPI 2.3.0.

New in OCPI 2.3.0 - Payment terminal support.
The CPO receives terminal information from PTP and assigns locations/EVSEs.
"""

from fastapi import APIRouter, Depends, Request

from py_ocpi.core import status
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.config import logger
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString
from py_ocpi.core.dependencies import get_adapter, get_crud
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import get_auth_token
from py_ocpi.modules.payments.v_2_3_0.schemas import (
    Terminal,
    TerminalPartialUpdate,
)
from py_ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/payments",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)


@router.get("/terminals/{terminal_id}", response_model=OCPIResponse)
async def get_terminal(
    request: Request,
    terminal_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get terminal by ID.

    Retrieves terminal details for validation purposes.

    **Path parameters:**
        - terminal_id (str): The ID of the terminal to retrieve.

    **Returns:**
        The OCPIResponse containing the terminal details.
    """
    logger.info("Received request to get terminal by id - `%s`." % terminal_id)
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.payments,
        RoleEnum.cpo,
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    if data:
        return OCPIResponse(
            data=[adapter.terminal_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Terminal with id `%s` was not found." % terminal_id)
    raise NotFoundOCPIError


@router.put("/terminals/{terminal_id}", response_model=OCPIResponse)
async def put_terminal(
    request: Request,
    terminal_id: CiString(36),  # type: ignore
    terminal: Terminal,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Create or update a terminal.

    **Path parameters:**
        - terminal_id (str): The ID of the terminal.

    **Request body:**
        - terminal (Terminal): The terminal object.

    **Returns:**
        The OCPIResponse containing the terminal details.
    """
    logger.info("Received request to put terminal with id - `%s`." % terminal_id)
    auth_token = get_auth_token(request)

    data = await crud.update(
        ModuleID.payments,
        RoleEnum.cpo,
        terminal.dict(),
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    return OCPIResponse(
        data=[adapter.terminal_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch("/terminals/{terminal_id}", response_model=OCPIResponse)
async def patch_terminal(
    request: Request,
    terminal_id: CiString(36),  # type: ignore
    terminal: TerminalPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Partially update a terminal.

    Used by CPO to assign location_ids and/or evse_uids to a terminal.

    **Path parameters:**
        - terminal_id (str): The ID of the terminal.

    **Request body:**
        - terminal (TerminalPartialUpdate): Partial terminal data.

    **Returns:**
        The OCPIResponse containing the updated terminal.
    """
    logger.info("Received request to patch terminal with id - `%s`." % terminal_id)
    auth_token = get_auth_token(request)

    data = await crud.update(
        ModuleID.payments,
        RoleEnum.cpo,
        terminal.dict(exclude_unset=True),
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    return OCPIResponse(
        data=[adapter.terminal_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
