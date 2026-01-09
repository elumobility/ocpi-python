from uuid import uuid4

from py_ocpi.core import enums
from py_ocpi.modules.tokens.v_2_3_0.enums import TokenType, WhitelistType
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/tokens/"
EMSP_BASE_URL = "/ocpi/emsp/2.3.0/tokens/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

TOKENS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "uid": str(uuid4()),
        "type": TokenType.rfid,
        "auth_id": str(uuid4()),
        "visual_number": None,
        "issuer": "Test Issuer",
        "group_id": None,
        "valid": True,
        "whitelist": WhitelistType.always,
        "language": None,
        "default_profile_type": None,
        "energy_contract": None,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]

AUTHORIZATION_INFO = {
    "allowed": "ALLOWED",
    "token": TOKENS[0],
    "location_id": None,
    "authorization_reference": None,
    "info": None,
}


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        if role == enums.RoleEnum.emsp and id is None:
            # For EMSP list endpoint
            return TOKENS
        return TOKENS[0]

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
        return TOKENS, 1, True

    @classmethod
    async def do(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        action: enums.Action,
        *args,
        data: dict = None,
        **kwargs,
    ):
        if action == enums.Action.authorize_token:
            return AUTHORIZATION_INFO
        return {}
