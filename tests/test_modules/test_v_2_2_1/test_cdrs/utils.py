from uuid import uuid4

from ocpi.core import enums
from ocpi.modules.cdrs.v_2_2_1.enums import AuthMethod, CdrDimensionType
from ocpi.modules.cdrs.v_2_2_1.schemas import TokenType
from ocpi.modules.locations.v_2_2_1.schemas import (
    ConnectorFormat,
    ConnectorType,
    PowerType,
)
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ENCODED_RANDOM_AUTH_TOKEN,
)

CPO_BASE_URL = "/ocpi/cpo/2.2.1/cdrs/"
EMSP_BASE_URL = "/ocpi/emsp/2.2.1/cdrs/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"}

CDRS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "id": str(uuid4()),
        "start_date_time": "2022-01-02 00:00:00+00:00",
        "end_date_time": "2022-01-02 00:05:00+00:00",
        "cdr_token": {
            "country_code": "us",
            "party_id": "AAA",
            "uid": str(uuid4()),
            "type": TokenType.rfid,
            "contract_id": str(uuid4()),
        },
        "auth_method": AuthMethod.auth_request,
        "cdr_location": {
            "id": str(uuid4()),
            "name": "name",
            "address": "address",
            "city": "city",
            "postal_code": "111111",
            "state": "state",
            "country": "USA",
            "coordinates": {
                "latitude": "latitude",
                "longitude": "longitude",
            },
            "evse_id": str(uuid4()),
            "connector_id": str(uuid4()),
            "connector_standard": ConnectorType.tesla_r,
            "connector_format": ConnectorFormat.cable,
            "connector_power_type": PowerType.dc,
        },
        "session_id": None,
        "authorization_reference": None,
        "meter_id": None,
        "currency": "MYR",
        "tariffs": [],
        "charging_periods": [
            {
                "start_date_time": "2022-01-02 00:00:00+00:00",
                "dimensions": [{"type": CdrDimensionType.power, "volume": 10}],
                "tariff_id": None,
            }
        ],
        "signed_data": None,
        "total_cost": {"excl_vat": 10.0000, "incl_vat": 10.2500},
        "total_fixed_cost": None,
        "total_energy": 50,
        "total_energy_cost": None,
        "total_time": 500,
        "total_time_cost": None,
        "total_parking_time": None,
        "total_parking_cost": None,
        "total_reservation_cost": None,
        "remark": None,
        "invoice_reference_id": None,
        "credit": None,
        "credit_reference_id": None,
        "home_charging_compensation": None,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return CDRS, 1, True

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return CDRS[0]

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
