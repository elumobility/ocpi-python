from uuid import uuid4

from ocpi.core import enums
from ocpi.modules.cdrs.v_2_3_0.enums import AuthMethod, CdrDimensionType
from ocpi.modules.cdrs.v_2_3_0.schemas import TokenType
from ocpi.modules.sessions.v_2_3_0.enums import SessionStatus
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/sessions/"
EMSP_BASE_URL = "/ocpi/emsp/2.3.0/sessions/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

SESSIONS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "id": str(uuid4()),
        "start_date_time": "2022-01-02 00:00:00+00:00",
        "end_date_time": "2022-01-02 00:05:00+00:00",
        "kwh": 100,
        "cdr_token": {
            "country_code": "us",
            "party_id": "AAA",
            "uid": str(uuid4()),
            "type": TokenType.rfid,
            "contract_id": str(uuid4()),
        },
        "auth_method": AuthMethod.auth_request,
        "authorization_reference": None,
        "location_id": str(uuid4()),
        "evse_uid": str(uuid4()),
        "connector_id": str(uuid4()),
        "meter_id": None,
        "currency": "MYR",
        "charging_periods": [
            {
                "start_date_time": "2022-01-02 00:00:00+00:00",
                "dimensions": [{"type": CdrDimensionType.power, "volume": 10}],
                "tariff_id": None,
            }
        ],
        "total_cost": {"excl_vat": 10.0000, "incl_vat": 10.2500},
        "status": SessionStatus.active,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return SESSIONS[0]

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
        return data

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
        return SESSIONS, 1, True
