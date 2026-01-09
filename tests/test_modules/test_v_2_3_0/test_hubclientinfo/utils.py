from py_ocpi.core import enums
from py_ocpi.modules.hubclientinfo.v_2_3_0.enums import ConnectionStatus
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/clientinfo/"
EMSP_BASE_URL = "/ocpi/emsp/2.3.0/clientinfo/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

HUB_CLIENT_INFO = {
    "party_id": "AAA",
    "country_code": "US",
    "role": enums.RoleEnum.cpo,
    "status": ConnectionStatus.connected,
    "last_updated": "2022-01-02 00:00:00+00:00",
}


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return HUB_CLIENT_INFO

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
        return [HUB_CLIENT_INFO], 1, True
