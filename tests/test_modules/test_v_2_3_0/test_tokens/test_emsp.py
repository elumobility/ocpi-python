from .utils import AUTH_HEADERS, EMSP_BASE_URL, TOKENS, WRONG_AUTH_HEADERS

GET_TOKEN_URL = EMSP_BASE_URL
PUT_TOKEN_URL = f'{EMSP_BASE_URL}{TOKENS[0]["uid"]}'
PATCH_TOKEN_URL = f'{EMSP_BASE_URL}{TOKENS[0]["uid"]}'
AUTHORIZE_TOKEN_URL = f'{EMSP_BASE_URL}{TOKENS[0]["uid"]}/authorize'


def test_emsp_get_token_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TOKEN_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_get_token_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TOKEN_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_emsp_authorize_token_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.post(
        AUTHORIZE_TOKEN_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_authorize_token_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.post(
        AUTHORIZE_TOKEN_URL,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["allowed"] == "ALLOWED"
