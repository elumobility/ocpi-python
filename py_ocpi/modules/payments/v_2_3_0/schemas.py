"""Schemas for payments module - OCPI 2.3.0.

New in OCPI 2.3.0 - Payment terminal support for direct payment.
https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc
"""

from typing import List, Optional

from pydantic import BaseModel

from py_ocpi.core.data_types import (
    CiString,
    DateTime,
    Price,
    URL,
)
from py_ocpi.modules.locations.schemas import GeoLocation
from py_ocpi.modules.payments.v_2_3_0.enums import (
    CaptureStatusCode,
    InvoiceCreator,
)


class Terminal(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc#terminal-object
    New in OCPI 2.3.0 - Describes a physical payment terminal.
    """

    terminal_id: CiString(max_length=36)  # type: ignore
    customer_reference: Optional[CiString(max_length=36)]  # type: ignore
    party_id: Optional[CiString(max_length=3)]  # type: ignore
    country_code: Optional[CiString(max_length=2)]  # type: ignore
    address: Optional[CiString(max_length=45)]  # type: ignore
    city: Optional[CiString(max_length=45)]  # type: ignore
    postal_code: Optional[CiString(max_length=10)]  # type: ignore
    state: Optional[CiString(max_length=20)]  # type: ignore
    country: Optional[CiString(max_length=3)]  # type: ignore
    coordinates: Optional[GeoLocation]
    invoice_base_url: Optional[URL]
    invoice_creator: Optional[InvoiceCreator]
    reference: Optional[CiString(max_length=36)]  # type: ignore
    location_ids: List[CiString(max_length=36)] = []  # type: ignore
    evse_uids: List[CiString(max_length=36)] = []  # type: ignore
    last_updated: DateTime


class TerminalPartialUpdate(BaseModel):
    """Partial update schema for Terminal object."""

    terminal_id: Optional[CiString(max_length=36)]  # type: ignore
    customer_reference: Optional[CiString(max_length=36)]  # type: ignore
    party_id: Optional[CiString(max_length=3)]  # type: ignore
    country_code: Optional[CiString(max_length=2)]  # type: ignore
    address: Optional[CiString(max_length=45)]  # type: ignore
    city: Optional[CiString(max_length=45)]  # type: ignore
    postal_code: Optional[CiString(max_length=10)]  # type: ignore
    state: Optional[CiString(max_length=20)]  # type: ignore
    country: Optional[CiString(max_length=3)]  # type: ignore
    coordinates: Optional[GeoLocation]
    invoice_base_url: Optional[URL]
    invoice_creator: Optional[InvoiceCreator]
    reference: Optional[CiString(max_length=36)]  # type: ignore
    location_ids: Optional[List[CiString(max_length=36)]]  # type: ignore
    evse_uids: Optional[List[CiString(max_length=36)]]  # type: ignore
    last_updated: Optional[DateTime]


class TerminalActivate(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc#terminalactivate-object
    Request body for terminal activation.
    """

    reference: CiString(max_length=36)  # type: ignore
    address: CiString(max_length=45)  # type: ignore
    city: CiString(max_length=45)  # type: ignore
    postal_code: Optional[CiString(max_length=10)]  # type: ignore
    state: Optional[CiString(max_length=20)]  # type: ignore
    country: CiString(max_length=3)  # type: ignore
    coordinates: Optional[GeoLocation]


class FinancialAdviceConfirmation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc#financial-advice-confirmation-object
    New in OCPI 2.3.0 - Encapsulates financial details of payment terminal transactions.
    """

    id: CiString(max_length=36)  # type: ignore
    authorization_reference: CiString(max_length=36)  # type: ignore
    total_costs: Price
    currency: CiString(max_length=3)  # type: ignore
    eft_data: List[CiString(max_length=255)]  # type: ignore
    capture_status_code: CaptureStatusCode
    capture_status_message: Optional[CiString(max_length=255)]  # type: ignore
    last_updated: DateTime
