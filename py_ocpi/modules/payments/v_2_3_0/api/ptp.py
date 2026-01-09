"""PTP (Payment Terminal Provider) API for payments module - OCPI 2.3.0.

New in OCPI 2.3.0 - Payment terminal support.
The PTP owns terminal data and financial advice confirmations.
"""

from fastapi import APIRouter, Depends, Request, Response

from py_ocpi.core import status
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.config import logger
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString
from py_ocpi.core.dependencies import get_adapter, get_crud, pagination_filters
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import get_auth_token, get_list
from py_ocpi.modules.payments.v_2_3_0.schemas import (
    FinancialAdviceConfirmation,
    Terminal,
    TerminalActivate,
)
from py_ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/payments",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)


# Terminal endpoints (PTP as sender)


@router.get("/terminals", response_model=OCPIResponse)
async def get_terminals(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get terminals.

    Retrieves a list of terminals based on the specified filters.

    **Query parameters:**
        - limit (int): Maximum number of objects to GET (default=50).
        - offset (int): The offset of the first object returned (default=0).
        - date_from (datetime): Only return Terminals that have
            last_updated after this Date/Time (default=None).
        - date_to (datetime): Only return Terminals that have
            last_updated before this Date/Time (default=None).

    **Returns:**
        The OCPIResponse containing the list of terminals.
    """
    logger.info("Received request to get terminals.")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.payments,
        RoleEnum.other,  # PTP role
        VersionNumber.v_2_3_0,
        crud,
        auth_token=auth_token,
    )

    terminals = []
    for data in data_list:
        terminals.append(
            adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()
        )
    logger.debug(f"Amount of terminals in response: {len(terminals)}")
    return OCPIResponse(
        data=terminals,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
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

    **Path parameters:**
        - terminal_id (str): The ID of the terminal to retrieve.

    **Returns:**
        The OCPIResponse containing the terminal details.
    """
    logger.info(f"Received request to get terminal by id - `{terminal_id}`.")
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.payments,
        RoleEnum.other,  # PTP role
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    if data:
        return OCPIResponse(
            data=[adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug(f"Terminal with id `{terminal_id}` was not found.")
    raise NotFoundOCPIError


@router.post("/terminals/activate", response_model=OCPIResponse)
async def activate_terminal(
    request: Request,
    terminal_activate: TerminalActivate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Activate a terminal.

    **Request body:**
        - terminal_activate (TerminalActivate): Terminal activation data.

    **Returns:**
        The OCPIResponse containing the activated terminal.
    """
    logger.info("Received request to activate terminal.")
    auth_token = get_auth_token(request)

    data = await crud.create(
        ModuleID.payments,
        RoleEnum.other,  # PTP role
        terminal_activate.model_dump(),
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
        operation="activate",
    )
    return OCPIResponse(
        data=[adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("/terminals/{terminal_id}/deactivate", response_model=OCPIResponse)
async def deactivate_terminal(
    request: Request,
    terminal_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Deactivate a terminal.

    **Path parameters:**
        - terminal_id (str): The ID of the terminal to deactivate.

    **Returns:**
        The OCPIResponse confirming deactivation.
    """
    logger.info(f"Received request to deactivate terminal - `{terminal_id}`.")
    auth_token = get_auth_token(request)

    data = await crud.update(
        ModuleID.payments,
        RoleEnum.other,  # PTP role
        {"status": "deactivated"},
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
        operation="deactivate",
    )
    return OCPIResponse(
        data=[adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


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
    logger.info(f"Received request to put terminal with id - `{terminal_id}`.")
    auth_token = get_auth_token(request)

    data = await crud.update(
        ModuleID.payments,
        RoleEnum.other,  # PTP role
        terminal.model_dump(),
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    return OCPIResponse(
        data=[adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


# Financial Advice Confirmation endpoints


@router.get("/financial-advice-confirmations", response_model=OCPIResponse)
async def get_financial_advice_confirmations(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get financial advice confirmations.

    **Query parameters:**
        - limit (int): Maximum number of objects to GET.
        - offset (int): The offset of the first object returned.
        - date_from (datetime): Filter by last_updated after this time.
        - date_to (datetime): Filter by last_updated before this time.

    **Returns:**
        The OCPIResponse containing the list of confirmations.
    """
    logger.info("Received request to get financial advice confirmations.")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.payments,
        RoleEnum.other,
        VersionNumber.v_2_3_0,
        crud,
        auth_token=auth_token,
        object_type="financial_advice_confirmation",
    )

    confirmations = []
    for data in data_list:
        confirmations.append(
            adapter.financial_advice_confirmation_adapter(
                data, VersionNumber.v_2_3_0
            ).model_dump()
        )
    return OCPIResponse(
        data=confirmations,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.get(
    "/financial-advice-confirmations/{confirmation_id}",
    response_model=OCPIResponse,
)
async def get_financial_advice_confirmation(
    request: Request,
    confirmation_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get financial advice confirmation by ID.

    **Path parameters:**
        - confirmation_id (str): The ID of the confirmation.

    **Returns:**
        The OCPIResponse containing the confirmation details.
    """
    logger.info(
        f"Received request to get financial advice confirmation - `{confirmation_id}`."
    )
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.payments,
        RoleEnum.other,
        confirmation_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
        object_type="financial_advice_confirmation",
    )
    if data:
        return OCPIResponse(
            data=[
                adapter.financial_advice_confirmation_adapter(
                    data, VersionNumber.v_2_3_0
                ).model_dump()
            ],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    raise NotFoundOCPIError


@router.put(
    "/financial-advice-confirmations/{confirmation_id}",
    response_model=OCPIResponse,
)
async def put_financial_advice_confirmation(
    request: Request,
    confirmation_id: CiString(36),  # type: ignore
    confirmation: FinancialAdviceConfirmation,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Create or update a financial advice confirmation.

    **Path parameters:**
        - confirmation_id (str): The ID of the confirmation.

    **Request body:**
        - confirmation (FinancialAdviceConfirmation): The confirmation object.

    **Returns:**
        The OCPIResponse containing the confirmation details.
    """
    logger.info(
        f"Received request to put financial advice confirmation - `{confirmation_id}`."
    )
    auth_token = get_auth_token(request)

    data = await crud.update(
        ModuleID.payments,
        RoleEnum.other,
        confirmation.model_dump(),
        confirmation_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
        object_type="financial_advice_confirmation",
    )
    return OCPIResponse(
        data=[
            adapter.financial_advice_confirmation_adapter(
                data, VersionNumber.v_2_3_0
            ).model_dump()
        ],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
