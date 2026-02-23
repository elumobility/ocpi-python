from .utils import (
    AUTH_HEADERS,
    EMSP_BASE_URL,
    FINANCIAL_ADVICE_CONFIRMATIONS,
    TERMINALS,
    WRONG_AUTH_HEADERS,
)

GET_TERMINALS_URL = f"{EMSP_BASE_URL}terminals"
GET_TERMINAL_URL = f"{EMSP_BASE_URL}terminals/{TERMINALS[0]['terminal_id']}"
GET_CONFIRMATIONS_URL = f"{EMSP_BASE_URL}financial-advice-confirmations"
GET_CONFIRMATION_URL = (
    f"{EMSP_BASE_URL}financial-advice-confirmations"
    f"/{FINANCIAL_ADVICE_CONFIRMATIONS[0]['id']}"
)


def test_emsp_get_terminals_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TERMINALS_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_get_terminals_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TERMINALS_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_emsp_get_terminal_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TERMINAL_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_get_terminal_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_TERMINAL_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["terminal_id"] == TERMINALS[0]["terminal_id"]


def test_emsp_get_financial_advice_confirmations_not_authenticated(
    client_emsp_v_2_3_0,
):
    response = client_emsp_v_2_3_0.get(
        GET_CONFIRMATIONS_URL, headers=WRONG_AUTH_HEADERS
    )

    assert response.status_code == 403


def test_emsp_get_financial_advice_confirmations_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_CONFIRMATIONS_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_emsp_get_financial_advice_confirmation_not_authenticated(
    client_emsp_v_2_3_0,
):
    response = client_emsp_v_2_3_0.get(GET_CONFIRMATION_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_get_financial_advice_confirmation_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.get(GET_CONFIRMATION_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == FINANCIAL_ADVICE_CONFIRMATIONS[0]["id"]
