from uuid import uuid4

from py_ocpi.core import enums
from py_ocpi.modules.chargingprofiles.v_2_3_0.enums import ChargingProfileResponseType
from tests.test_modules.test_v_2_3_0.test_sessions.utils import SESSIONS

from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/chargingprofiles/"
EMSP_BASE_URL = "/ocpi/emsp/2.3.0/chargingprofiles/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

SET_CHARGING_PROFILE = {
    "response_url": "https://example.com/ocpi/v2.3.0/chargingprofiles/123",
    "charging_profile": {
        "charging_rate_unit": "W",
        "min_charge_rate": 1,
        "charging_profile_period": {
            "start_period": 1,
            "limit": 1,
        },
    },
}


class Crud:
    @classmethod
    async def do(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        action: enums.Action,
        *args,
        data: dict = None,
        **kwargs,
    ) -> dict:
        if module == enums.ModuleID.charging_profile:
            return {"result": "ACCEPTED", "timeout": 0}
        return {}

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        if module == enums.ModuleID.sessions:
            return SESSIONS[0]
        return SET_CHARGING_PROFILE

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        id,
        *args,
        **kwargs,
    ) -> dict:
        return data

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        *args,
        **kwargs,
    ) -> dict:
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
        return [], 0, False
