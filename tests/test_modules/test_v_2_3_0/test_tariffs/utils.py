from uuid import uuid4

from py_ocpi.core import enums
from py_ocpi.modules.tariffs.v_2_3_0.enums import TariffDimensionType
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/tariffs/"
EMSP_BASE_URL = "/ocpi/emsp/2.3.0/tariffs/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

TARIFFS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "id": str(uuid4()),
        "currency": "EUR",
        "tariff_alt_text": [],
        "tariff_alt_url": None,
        "min_price": None,
        "max_price": None,
        "elements": [
            {
                "price_components": [
                    {
                        "type": TariffDimensionType.energy,
                        "price": 0.5,
                        "step_size": 1,
                        "vat": None,
                    }
                ],
                "restrictions": None,
            }
        ],
        "start_date_time": None,
        "end_date_time": None,
        "energy_mix": None,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return TARIFFS[0]

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
        return TARIFFS, 1, True
