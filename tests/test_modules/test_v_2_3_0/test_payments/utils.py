from uuid import uuid4

from ocpi.core import enums
from ocpi.modules.payments.v_2_3_0.enums import CaptureStatusCode
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/payments/"
PTP_BASE_URL = "/ocpi/ptp/2.3.0/payments/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

TERMINALS = [
    {
        "terminal_id": str(uuid4()),
        "customer_reference": None,
        "party_id": None,
        "country_code": None,
        "address": None,
        "city": None,
        "postal_code": None,
        "state": None,
        "country": None,
        "coordinates": None,
        "invoice_base_url": None,
        "invoice_creator": None,
        "reference": None,
        "location_ids": [],
        "evse_uids": [],
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]

FINANCIAL_ADVICE_CONFIRMATIONS = [
    {
        "id": str(uuid4()),
        "authorization_reference": str(uuid4()),
        "total_costs": {"excl_vat": 10.0, "incl_vat": 12.0},
        "currency": "EUR",
        "eft_data": ["data1", "data2"],
        "capture_status_code": CaptureStatusCode.success,
        "capture_status_message": None,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return TERMINALS[0]

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        id,
        *args,
        **kwargs,
    ):
        # For financial advice confirmations, return the confirmation data
        if kwargs.get("object_type") == "financial_advice_confirmation":
            updated = FINANCIAL_ADVICE_CONFIRMATIONS[0].copy()
            updated.update(data)
            return updated
        # For terminals, merge with existing terminal data
        updated = TERMINALS[0].copy()
        updated.update(data)
        return updated

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        *args,
        **kwargs,
    ):
        return data

    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        # Check if it's financial advice confirmations
        if kwargs.get("object_type") == "financial_advice_confirmation":
            return FINANCIAL_ADVICE_CONFIRMATIONS, 1, True
        return TERMINALS, 1, True
