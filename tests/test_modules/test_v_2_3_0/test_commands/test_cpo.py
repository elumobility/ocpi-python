import datetime
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from ocpi import get_application
from ocpi.core import enums
from ocpi.core.exceptions import NotFoundOCPIError
from ocpi.modules.commands.v_2_3_0.enums import (
    CommandResultType,
    CommandType,
)
from ocpi.modules.tokens.v_2_3_0.enums import TokenType, WhitelistType
from ocpi.modules.versions.enums import VersionNumber
from tests.test_modules.utils import ClientAuthenticator

from .utils import (
    AUTH_HEADERS,
    COMMAND_RESPONSE,
    COMMAND_RESULT,
    CPO_BASE_URL,
    WRONG_AUTH_HEADERS,
    Crud,
)

COMMAND_START_URL = f"{CPO_BASE_URL}{CommandType.start_session.value}"
COMMAND_STOP_URL = f"{CPO_BASE_URL}{CommandType.stop_session.value}"
RESERVE_NOW_URL = f"{CPO_BASE_URL}{CommandType.reserve_now.value}"


@pytest.mark.parametrize(
    "endpoint",
    [
        COMMAND_START_URL,
        COMMAND_STOP_URL,
        RESERVE_NOW_URL,
    ],
)
def test_cpo_receive_command_start_session_not_authenticated(
    client_cpo_v_2_3_0,
    endpoint,
):
    response = client_cpo_v_2_3_0.post(
        endpoint,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_receive_command_start_session_v_2_3_0(client_cpo_v_2_3_0):
    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": {
            "country_code": "us",
            "party_id": "AAA",
            "uid": str(uuid4()),
            "type": TokenType.rfid,
            "contract_id": str(uuid4()),
            "issuer": "company",
            "valid": True,
            "whitelist": WhitelistType.always,
            "visual_number": None,
            "group_id": None,
            "language": None,
            "default_profile_type": None,
            "energy_contract": None,
            "last_updated": "2022-01-02 00:00:00+00:00",
        },
        "location_id": str(uuid4()),
        "evse_uid": None,
        "connector_id": None,
        "authorization_reference": None,
    }

    response = client_cpo_v_2_3_0.post(
        COMMAND_START_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_stop_session_v_2_3_0(client_cpo_v_2_3_0):
    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "session_id": str(uuid4()),
    }

    response = client_cpo_v_2_3_0.post(
        COMMAND_STOP_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_v_2_3_0(client_cpo_v_2_3_0):
    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": {
            "country_code": "us",
            "party_id": "AAA",
            "uid": str(uuid4()),
            "type": TokenType.rfid,
            "contract_id": str(uuid4()),
            "issuer": "company",
            "valid": True,
            "whitelist": WhitelistType.always,
            "visual_number": None,
            "group_id": None,
            "language": None,
            "default_profile_type": None,
            "energy_contract": None,
            "last_updated": "2022-01-02 00:00:00+00:00",
        },
        "expiry_date": str(datetime.datetime.now() + datetime.timedelta(days=1)),
        "reservation_id": str(uuid4()),
        "location_id": str(uuid4()),
        "evse_uid": None,
        "authorization_reference": None,
    }

    response = client_cpo_v_2_3_0.post(
        RESERVE_NOW_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_unknown_location_v_2_3_0():
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        if module == enums.ModuleID.commands:
            return COMMAND_RESULT
        if module == enums.ModuleID.locations:
            raise NotFoundOCPIError()

    _get = Crud.get
    Crud.get = get

    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.commands],
    )

    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": {
            "country_code": "us",
            "party_id": "AAA",
            "uid": str(uuid4()),
            "type": TokenType.rfid,
            "contract_id": str(uuid4()),
            "issuer": "company",
            "valid": True,
            "whitelist": WhitelistType.always,
            "visual_number": None,
            "group_id": None,
            "language": None,
            "default_profile_type": None,
            "energy_contract": None,
            "last_updated": "2022-01-02 00:00:00+00:00",
        },
        "expiry_date": str(datetime.datetime.now() + datetime.timedelta(days=1)),
        "reservation_id": str(uuid4()),
        "location_id": str(uuid4()),
        "evse_uid": None,
        "authorization_reference": None,
    }

    client = TestClient(app)
    response = client.post(
        RESERVE_NOW_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["result"] == CommandResultType.rejected

    # revert Crud changes
    Crud.get = _get
