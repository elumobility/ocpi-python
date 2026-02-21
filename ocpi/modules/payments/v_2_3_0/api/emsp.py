"""EMSP API for payments module - OCPI 2.3.0.

The EMSP is the Sender for the Payments module. It pulls terminal
and financial advice confirmation data from the CPO.

Sender interface (EMSP):
  Terminals              - GET list, GET by ID
  FinancialAdvice        - GET list, GET by ID

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
    Get terminals (EMSP).

    Retrieves a list of terminals from the CPO.

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
    logger.info("Received request to get terminals (EMSP).")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.payments,
        RoleEnum.emsp,
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
    Get terminal by ID (EMSP).

    **Path parameters:**
        - terminal_id (str): The ID of the terminal to retrieve.

    **Returns:**
        The OCPIResponse containing the terminal details.
    """
    logger.info(f"Received request to get terminal by id - `{terminal_id}` (EMSP).")
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.payments,
        RoleEnum.emsp,
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
    Get financial advice confirmations (EMSP).

    **Query parameters:**
        - limit (int): Maximum number of objects to GET.
        - offset (int): The offset of the first object returned.
        - date_from (datetime): Filter by last_updated after this time.
        - date_to (datetime): Filter by last_updated before this time.

    **Returns:**
        The OCPIResponse containing the list of confirmations.
    """
    logger.info("Received request to get financial advice confirmations (EMSP).")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.payments,
        RoleEnum.emsp,
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
    Get financial advice confirmation by ID (EMSP).

    **Path parameters:**
        - confirmation_id (str): The ID of the confirmation.

    **Returns:**
        The OCPIResponse containing the confirmation details.
    """
    logger.info(
        f"Received request to get financial advice confirmation"
        f" - `{confirmation_id}` (EMSP)."
    )
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.payments,
        RoleEnum.emsp,
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
