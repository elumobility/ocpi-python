from ocpi.core import enums
from ocpi.modules.commands.v_2_3_0.enums import (
    CommandResponseType,
    CommandResultType,
)
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/commands/"
EMSP_BASE_URL = "/ocpi/emsp/2.3.0/commands/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

COMMAND_RESPONSE = {"result": CommandResponseType.accepted, "timeout": 30}

COMMAND_RESULT = {"result": CommandResultType.accepted}


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
        if action == enums.Action.get_client_token:
            return "foo"

        return COMMAND_RESPONSE

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        return COMMAND_RESULT

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
