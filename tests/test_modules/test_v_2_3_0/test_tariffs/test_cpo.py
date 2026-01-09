from .utils import AUTH_HEADERS, CPO_BASE_URL, TARIFFS, WRONG_AUTH_HEADERS

GET_TARIFFS_URL = CPO_BASE_URL


def test_cpo_get_tariffs_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(GET_TARIFFS_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_cpo_get_tariffs_v_2_3_0(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(GET_TARIFFS_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == TARIFFS[0]["id"]
