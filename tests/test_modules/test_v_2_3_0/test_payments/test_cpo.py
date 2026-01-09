from .utils import AUTH_HEADERS, CPO_BASE_URL, TERMINALS, WRONG_AUTH_HEADERS

GET_TERMINAL_URL = f'{CPO_BASE_URL}terminals/{TERMINALS[0]["terminal_id"]}'


def test_cpo_get_terminal_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(GET_TERMINAL_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_cpo_get_terminal_v_2_3_0(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(GET_TERMINAL_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["terminal_id"] == TERMINALS[0]["terminal_id"]
