from uuid import uuid4

from .utils import (
    AUTH_HEADERS,
    FINANCIAL_ADVICE_CONFIRMATIONS,
    PTP_BASE_URL,
    TERMINALS,
    WRONG_AUTH_HEADERS,
)

GET_TERMINALS_URL = f"{PTP_BASE_URL}terminals"
GET_TERMINAL_URL = f"{PTP_BASE_URL}terminals/{TERMINALS[0]['terminal_id']}"
POST_TERMINAL_URL = f"{PTP_BASE_URL}terminals/{TERMINALS[0]['terminal_id']}"
PATCH_TERMINAL_URL = f"{PTP_BASE_URL}terminals/{TERMINALS[0]['terminal_id']}"
FINANCIAL_ADVICE_URL = f"{PTP_BASE_URL}financial-advice-confirmations/{FINANCIAL_ADVICE_CONFIRMATIONS[0]['id']}"


def test_ptp_get_terminals_not_authenticated(client_ptp_v_2_3_0):
    response = client_ptp_v_2_3_0.get(GET_TERMINALS_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_ptp_get_terminals_v_2_3_0(client_ptp_v_2_3_0):
    response = client_ptp_v_2_3_0.get(GET_TERMINALS_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["terminal_id"] == TERMINALS[0]["terminal_id"]


def test_ptp_get_terminal_v_2_3_0(client_ptp_v_2_3_0):
    response = client_ptp_v_2_3_0.get(GET_TERMINAL_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["terminal_id"] == TERMINALS[0]["terminal_id"]


def test_ptp_post_terminal_not_authenticated(client_ptp_v_2_3_0):
    response = client_ptp_v_2_3_0.put(
        POST_TERMINAL_URL,
        json=TERMINALS[0],
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_ptp_post_terminal_v_2_3_0(client_ptp_v_2_3_0):
    response = client_ptp_v_2_3_0.put(
        POST_TERMINAL_URL,
        json=TERMINALS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["terminal_id"] == TERMINALS[0]["terminal_id"]


# Note: PTP role doesn't have PATCH endpoint for terminals, only PUT
# These tests are skipped as PATCH is not available for PTP terminals
def test_ptp_patch_terminal_not_authenticated(client_ptp_v_2_3_0):
    # PATCH endpoint doesn't exist for PTP terminals
    response = client_ptp_v_2_3_0.patch(
        PATCH_TERMINAL_URL,
        json={"id": str(uuid4())},
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 405  # Method Not Allowed


def test_ptp_patch_terminal_v_2_3_0(client_ptp_v_2_3_0):
    # PATCH endpoint doesn't exist for PTP terminals
    patch_data = {"terminal_id": str(uuid4())}
    response = client_ptp_v_2_3_0.patch(
        PATCH_TERMINAL_URL,
        json=patch_data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 405  # Method Not Allowed


def test_ptp_post_financial_advice_not_authenticated(client_ptp_v_2_3_0):
    response = client_ptp_v_2_3_0.put(
        FINANCIAL_ADVICE_URL,
        json=FINANCIAL_ADVICE_CONFIRMATIONS[0],
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_ptp_post_financial_advice_v_2_3_0(client_ptp_v_2_3_0):
    response = client_ptp_v_2_3_0.put(
        FINANCIAL_ADVICE_URL,
        json=FINANCIAL_ADVICE_CONFIRMATIONS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
