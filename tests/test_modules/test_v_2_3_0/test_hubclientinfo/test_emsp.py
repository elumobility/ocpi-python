import pytest

from .utils import HUB_CLIENT_INFO, AUTH_HEADERS, WRONG_AUTH_HEADERS, EMSP_BASE_URL

GET_HUB_CLIENT_INFO_URL = f'{EMSP_BASE_URL}{HUB_CLIENT_INFO["country_code"]}/{HUB_CLIENT_INFO["party_id"]}'
PUT_HUB_CLIENT_INFO_URL = f'{EMSP_BASE_URL}{HUB_CLIENT_INFO["country_code"]}/{HUB_CLIENT_INFO["party_id"]}'


def test_emsp_get_hubclientinfo_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(
        GET_HUB_CLIENT_INFO_URL, headers=WRONG_AUTH_HEADERS
    )

    assert response.status_code == 403


def test_emsp_get_hubclientinfo_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_HUB_CLIENT_INFO_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["party_id"] == HUB_CLIENT_INFO["party_id"]


def test_emsp_put_hubclientinfo_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.put(
        PUT_HUB_CLIENT_INFO_URL,
        json=HUB_CLIENT_INFO,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_put_hubclientinfo_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.put(
        PUT_HUB_CLIENT_INFO_URL,
        json=HUB_CLIENT_INFO,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["party_id"] == HUB_CLIENT_INFO["party_id"]
