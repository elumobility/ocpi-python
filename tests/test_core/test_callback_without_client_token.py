"""Result callbacks are skipped when the CPO has no token for the caller.

``crud.do(Action.get_client_token)`` returns None when the CPO cannot identify
the calling party. Encoding None used to raise a TypeError inside the
background task; sending another party's token instead would leak it. Every
callback now returns early: no waiting for the result, no HTTP request.
"""

import inspect
from collections.abc import Callable
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from ocpi.modules.chargingprofiles.v_2_2_1 import background_tasks as profiles_221
from ocpi.modules.chargingprofiles.v_2_3_0 import background_tasks as profiles_230
from ocpi.modules.commands.v_2_1_1.api import cpo as commands_211
from ocpi.modules.commands.v_2_2_1.api import cpo as commands_221
from ocpi.modules.commands.v_2_3_0.api import cpo as commands_230

CALLBACKS = [
    commands_211.send_command_result,
    commands_221.send_command_result,
    commands_230.send_command_result,
    profiles_221.send_get_chargingprofile,
    profiles_221.send_update_chargingprofile,
    profiles_221.send_delete_chargingprofile,
    profiles_230.send_get_chargingprofile,
    profiles_230.send_update_chargingprofile,
    profiles_230.send_delete_chargingprofile,
]


class NoClientTokenCrud:
    """A CPO crud that cannot identify the caller, recording result polls."""

    def __init__(self) -> None:
        self.result_polls = 0

    async def do(self, *args: Any, **kwargs: Any) -> None:
        return None

    async def get(self, *args: Any, **kwargs: Any) -> None:
        self.result_polls += 1
        return None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "callback", CALLBACKS, ids=lambda f: f"{f.__module__}.{f.__name__}"
)
async def test_callback_is_skipped_without_a_client_token(
    callback: Callable[..., Any],
) -> None:
    crud = NoClientTokenCrud()
    arguments = {
        name: crud if name == "crud" else MagicMock()
        for name in inspect.signature(callback).parameters
    }

    with patch(f"{callback.__module__}.httpx.AsyncClient") as http_client:
        await callback(**arguments)

    http_client.assert_not_called()
    assert crud.result_polls == 0
