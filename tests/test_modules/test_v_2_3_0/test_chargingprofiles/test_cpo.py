from unittest.mock import patch

from ocpi.modules.chargingprofiles.v_2_3_0.enums import ChargingProfileResponseType
from tests.test_modules.test_v_2_3_0.test_sessions.utils import SESSIONS

from .utils import (
    AUTH_HEADERS,
    CPO_BASE_URL,
    SET_CHARGING_PROFILE,
    WRONG_AUTH_HEADERS,
)

CHARGINGPROFILE_URL = f"{CPO_BASE_URL}{SESSIONS[0]['id']}"


def test_cpo_set_charging_profile_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.put(
        CHARGINGPROFILE_URL,
        json=SET_CHARGING_PROFILE,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


@patch("ocpi.modules.chargingprofiles.v_2_3_0.api.cpo.BackgroundTasks.add_task")
def test_cpo_set_charging_profile_v_2_3_0(mock_background, client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.put(
        CHARGINGPROFILE_URL,
        json=SET_CHARGING_PROFILE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == ChargingProfileResponseType.accepted
    assert mock_background.call_count == 1


@patch("ocpi.modules.chargingprofiles.v_2_3_0.api.cpo.BackgroundTasks.add_task")
def test_cpo_clear_charging_profile_v_2_3_0(mock_background, client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.delete(
        f"{CHARGINGPROFILE_URL}?response_url=https://example.com/response",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == ChargingProfileResponseType.accepted
    assert mock_background.call_count == 1
