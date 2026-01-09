from uuid import uuid4

from ocpi.core import enums
from ocpi.modules.tokens.v_2_2_1.enums import (
    AllowedType,
    TokenType,
    WhitelistType,
)
from ocpi.modules.tokens.v_2_2_1.schemas import AuthorizationInfo, Token
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ENCODED_RANDOM_AUTH_TOKEN,
)

CPO_BASE_URL = "/ocpi/cpo/2.2.1/tokens/"
EMSP_BASE_URL = "/ocpi/emsp/2.2.1/tokens/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"}

TOKENS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "uid": str(uuid4()),
        "type": TokenType.rfid,
        "contract_id": str(uuid4()),
        "visual_number": None,
        "issuer": "issuer",
        "group_id": None,
        "valid": True,
        "whitelist": WhitelistType.always,
        "language": None,
        "default_profile_type": None,
        "energy_contract": None,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]

TOKEN_UPDATE = {
    "country_code": "pl",
    "party_id": "BBB",
    "last_updated": "2022-01-02 00:00:00+00:00",
}


class Crud:
    @classmethod
    async def get(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> Token:
        return TOKENS[0]

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: Token,
        *args,
        **kwargs,
    ) -> dict:
        return data

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
        token = Token(**TOKENS[0])
        auth_info = AuthorizationInfo(
            allowed=AllowedType.allowed,
            token=token,
            location=None,
            authorization_reference=None,
            info=None,
        )
        return auth_info.model_dump()

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
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: Token,
        id: str,
        *args,
        **kwargs,
    ):
        data = dict(data)
        TOKENS[0]["country_code"] = data["country_code"]
        TOKENS[0]["party_id"] = data["party_id"]
        return TOKENS[0]
