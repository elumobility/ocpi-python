"""CPO API for payments module - OCPI 2.3.0.

New in OCPI 2.3.0 - Payment terminal support.

The CPO is the Receiver for the Payments module. It receives terminal
information and financial advice confirmations from the PTP.

Receiver interface (CPO):
  Terminals              - GET list, GET by ID, PUT, PATCH
  FinancialAdvice        - GET list, GET by ID, PUT

Reference: https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc
"""

from fastapi import APIRouter, Depends, Request, Response

from ocpi.core import status
from ocpi.core.adapter import Adapter
from ocpi.core.authentication.verifier import AuthorizationVerifier
from ocpi.core.config import logger
from ocpi.core.crud import Crud
from ocpi.core.data_types import CiString
from ocpi.core.dependencies import get_adapter, get_crud, pagination_filters
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.exceptions import NotFoundOCPIError
from ocpi.core.schemas import OCPIResponse
from ocpi.core.utils import get_auth_token, get_list
from ocpi.modules.payments.v_2_3_0.schemas import (
    FinancialAdviceConfirmation,
    Terminal,
    TerminalPartialUpdate,
)
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/payments",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)


# ---------------------------------------------------------------------------
# Terminal endpoints
# ---------------------------------------------------------------------------


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

    Retrieves a list of terminals known to this CPO.

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
    logger.info("Received request to get terminals (CPO).")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.payments,
        RoleEnum.cpo,
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

    Retrieves terminal details for validation purposes.

    **Path parameters:**
        - terminal_id (str): The ID of the terminal to retrieve.

    **Returns:**
        The OCPIResponse containing the terminal details.
    """
    logger.info(f"Received request to get terminal by id - `{terminal_id}`.")
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
            data=[adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug(f"Terminal with id `{terminal_id}` was not found.")
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

    Called by the PTP to push terminal data to the CPO.

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
        RoleEnum.cpo,
        terminal.model_dump(),
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    return OCPIResponse(
        data=[adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()],
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
    logger.info(f"Received request to patch terminal with id - `{terminal_id}`.")
    auth_token = get_auth_token(request)

    data = await crud.update(
        ModuleID.payments,
        RoleEnum.cpo,
        terminal.model_dump(exclude_unset=True),
        terminal_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_3_0,
    )
    return OCPIResponse(
        data=[adapter.terminal_adapter(data, VersionNumber.v_2_3_0).model_dump()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


# ---------------------------------------------------------------------------
# Financial Advice Confirmation endpoints
# ---------------------------------------------------------------------------


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

    Retrieves a list of financial advice confirmations received by this CPO.

    **Query parameters:**
        - limit (int): Maximum number of objects to GET.
        - offset (int): The offset of the first object returned.
        - date_from (datetime): Filter by last_updated after this time.
        - date_to (datetime): Filter by last_updated before this time.

    **Returns:**
        The OCPIResponse containing the list of confirmations.
    """
    logger.info("Received request to get financial advice confirmations (CPO).")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.payments,
        RoleEnum.cpo,
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
        RoleEnum.cpo,
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

    Called by the PTP to push a financial advice confirmation to the CPO
    after a payment transaction is completed at a terminal.

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
        RoleEnum.cpo,
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
