from .utils import AUTH_HEADERS, CPO_BASE_URL, HUB_CLIENT_INFO, WRONG_AUTH_HEADERS

GET_HUB_CLIENT_INFO_URL = (
    f"{CPO_BASE_URL}{HUB_CLIENT_INFO['country_code']}/{HUB_CLIENT_INFO['party_id']}"
)
PUT_HUB_CLIENT_INFO_URL = (
    f"{CPO_BASE_URL}{HUB_CLIENT_INFO['country_code']}/{HUB_CLIENT_INFO['party_id']}"
)


def test_cpo_get_hubclientinfo_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(
        GET_HUB_CLIENT_INFO_URL, headers=WRONG_AUTH_HEADERS
    )

    assert response.status_code == 403


def test_cpo_get_hubclientinfo_v_2_3_0(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(GET_HUB_CLIENT_INFO_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["party_id"] == HUB_CLIENT_INFO["party_id"]


def test_cpo_put_hubclientinfo_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.put(
        PUT_HUB_CLIENT_INFO_URL,
        json=HUB_CLIENT_INFO,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_put_hubclientinfo_v_2_3_0(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.put(
        PUT_HUB_CLIENT_INFO_URL,
        json=HUB_CLIENT_INFO,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["party_id"] == HUB_CLIENT_INFO["party_id"]
