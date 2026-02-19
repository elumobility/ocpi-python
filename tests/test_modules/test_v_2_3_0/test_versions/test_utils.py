from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
)

AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}
