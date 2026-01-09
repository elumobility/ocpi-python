from .utils import AUTH_HEADERS, CPO_BASE_URL, TOKENS, WRONG_AUTH_HEADERS

GET_TOKEN_URL = f"{CPO_BASE_URL}{TOKENS[0]['country_code']}/{TOKENS[0]['party_id']}/{TOKENS[0]['uid']}"
PUT_TOKEN_URL = f"{CPO_BASE_URL}{TOKENS[0]['country_code']}/{TOKENS[0]['party_id']}/{TOKENS[0]['uid']}"
PATCH_TOKEN_URL = f"{CPO_BASE_URL}{TOKENS[0]['country_code']}/{TOKENS[0]['party_id']}/{TOKENS[0]['uid']}"


def test_cpo_get_token_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(GET_TOKEN_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_cpo_get_token_v_2_3_0(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.get(GET_TOKEN_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_cpo_put_token_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.put(
        PUT_TOKEN_URL,
        json=TOKENS[0],
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_put_token_v_2_3_0(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.put(
        PUT_TOKEN_URL,
        json=TOKENS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_cpo_patch_token_not_authenticated(client_cpo_v_2_3_0):
    response = client_cpo_v_2_3_0.patch(
        PATCH_TOKEN_URL,
        json={"uid": TOKENS[0]["uid"]},
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_patch_token_v_2_3_0(client_cpo_v_2_3_0):
    patch_data = {"uid": TOKENS[0]["uid"], "valid": False}
    response = client_cpo_v_2_3_0.patch(
        PATCH_TOKEN_URL,
        json=patch_data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]
