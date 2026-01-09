from .utils import (
    COMMAND_RESPONSE,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
    EMSP_BASE_URL,
)

RECEIVE_URL = f"{EMSP_BASE_URL}1234"


def test_emsp_receive_command_result_not_authenticated(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.post(
        RECEIVE_URL,
        json=COMMAND_RESPONSE,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_receive_command_result_v_2_3_0(client_emsp_v_2_3_0):
    response = client_emsp_v_2_3_0.post(
        RECEIVE_URL,
        json=COMMAND_RESPONSE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
