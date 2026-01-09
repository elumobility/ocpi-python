import pytest

from .utils import TARIFFS, AUTH_HEADERS, WRONG_AUTH_HEADERS, EMSP_BASE_URL

GET_TARIFF_URL = f'{EMSP_BASE_URL}{TARIFFS[0]["country_code"]}/{TARIFFS[0]["party_id"]}/{TARIFFS[0]["id"]}'


def test_emsp_get_tariff_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TARIFF_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_get_tariff_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TARIFF_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == TARIFFS[0]["id"]
