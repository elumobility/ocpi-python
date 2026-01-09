from uuid import uuid4

from py_ocpi.core import enums
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/credentials/"
EMSP_BASE_URL = "/ocpi/emsp/2.3.0/credentials/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

CREDENTIALS_TOKEN_CREATE = {
    "token": str(uuid4()),
    "url": "https://example.com/ocpi/v2.3.0",
    "roles": [
        {
            "role": enums.RoleEnum.emsp,
            "business_details": {
                "name": "Test Company",
                "website": None,
                "logo": None,
            },
            "party_id": "AAA",
            "country_code": "us",
        }
    ],
}

CREDENTIALS_TOKEN_GET = {
    "token": str(uuid4()),
    "url": "https://example.com/ocpi/v2.3.0",
    "roles": [
        {
            "role": enums.RoleEnum.emsp,
            "business_details": {
                "name": "Test Company",
                "website": None,
                "logo": None,
            },
            "party_id": "AAA",
            "country_code": "us",
        }
    ],
}


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return CREDENTIALS_TOKEN_CREATE

    @classmethod
    async def create(cls, module: enums.ModuleID, data, operation, *args, **kwargs):
        if operation == "credentials":
            return None
        return CREDENTIALS_TOKEN_CREATE

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
        # Return server credentials for POST credentials endpoint
        if action == enums.Action.get_client_token:
            return CREDENTIALS_TOKEN_GET
        return None
