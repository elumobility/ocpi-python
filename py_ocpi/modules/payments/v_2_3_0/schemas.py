"""Schemas for payments module - OCPI 2.3.0.

New in OCPI 2.3.0 - Payment terminal support for direct payment.
https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc
"""


from pydantic import BaseModel

from py_ocpi.core.data_types import (
    URL,
    CiString,
    DateTime,
    Price,
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
    customer_reference: CiString(max_length=36) | None  # type: ignore
    party_id: CiString(max_length=3) | None  # type: ignore
    country_code: CiString(max_length=2) | None  # type: ignore
    address: CiString(max_length=45) | None  # type: ignore
    city: CiString(max_length=45) | None  # type: ignore
    postal_code: CiString(max_length=10) | None  # type: ignore
    state: CiString(max_length=20) | None  # type: ignore
    country: CiString(max_length=3) | None  # type: ignore
    coordinates: GeoLocation | None
    invoice_base_url: URL | None
    invoice_creator: InvoiceCreator | None
    reference: CiString(max_length=36) | None  # type: ignore
    location_ids: list[CiString(max_length=36)] = []  # type: ignore
    evse_uids: list[CiString(max_length=36)] = []  # type: ignore
    last_updated: DateTime


class TerminalPartialUpdate(BaseModel):
    """Partial update schema for Terminal object."""

    terminal_id: CiString(max_length=36) | None = None  # type: ignore
    customer_reference: CiString(max_length=36) | None = None  # type: ignore
    party_id: CiString(max_length=3) | None = None  # type: ignore
    country_code: CiString(max_length=2) | None = None  # type: ignore
    address: CiString(max_length=45) | None = None  # type: ignore
    city: CiString(max_length=45) | None = None  # type: ignore
    postal_code: CiString(max_length=10) | None = None  # type: ignore
    state: CiString(max_length=20) | None = None  # type: ignore
    country: CiString(max_length=3) | None = None  # type: ignore
    coordinates: GeoLocation | None = None
    invoice_base_url: URL | None = None
    invoice_creator: InvoiceCreator | None = None
    reference: CiString(max_length=36) | None = None  # type: ignore
    location_ids: list[CiString(max_length=36)] | None = None  # type: ignore
    evse_uids: list[CiString(max_length=36)] | None = None  # type: ignore
    last_updated: DateTime | None = None


class TerminalActivate(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc#terminalactivate-object
    Request body for terminal activation.
    """

    reference: CiString(max_length=36)  # type: ignore
    address: CiString(max_length=45)  # type: ignore
    city: CiString(max_length=45)  # type: ignore
    postal_code: CiString(max_length=10) | None  # type: ignore
    state: CiString(max_length=20) | None  # type: ignore
    country: CiString(max_length=3)  # type: ignore
    coordinates: GeoLocation | None


class FinancialAdviceConfirmation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc#financial-advice-confirmation-object
    New in OCPI 2.3.0 - Encapsulates financial details of payment terminal transactions.
    """

    id: CiString(max_length=36)  # type: ignore
    authorization_reference: CiString(max_length=36)  # type: ignore
    total_costs: Price
    currency: CiString(max_length=3)  # type: ignore
    eft_data: list[CiString(max_length=255)]  # type: ignore
    capture_status_code: CaptureStatusCode
    capture_status_message: CiString(max_length=255) | None  # type: ignore
    last_updated: DateTime
