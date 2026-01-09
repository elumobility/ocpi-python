"""Enums for payments module - OCPI 2.3.0.

New in OCPI 2.3.0 - Payment terminal support.
https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc
"""

from enum import Enum


class InvoiceCreator(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc#invoicecreator-enum
    Describes which party creates the invoice for the eDriver.
    """

    # The CPO creates the invoice
    cpo = "CPO"
    # The PTP creates the invoice
    ptp = "PTP"


class CaptureStatusCode(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_payments.asciidoc#capturestatuscode-enum
    Code that identifies the financial advice status.
    """

    # Capture was successful
    success = "SUCCESS"
    # Capture failed
    failed = "FAILED"
    # Capture is pending
    pending = "PENDING"
