"""Tests for ocpi.core.authentication.verifier module."""

from unittest.mock import patch

import pytest
from fastapi import WebSocketException, status

from ocpi.core.authentication.authenticator import Authenticator
from ocpi.core.authentication.verifier import (
    AuthorizationVerifier,
    CredentialsAuthorizationVerifier,
    HttpPushVerifier,
    VersionsAuthorizationVerifier,
    WSPushVerifier,
)
from ocpi.core.exceptions import AuthorizationOCPIError
from ocpi.modules.versions.enums import VersionNumber


class MockAuthenticator(Authenticator):
    """Mock authenticator for testing."""

    @classmethod
    async def get_valid_token_c(cls) -> list[str]:
        return ["valid_token_c"]

    @classmethod
    async def get_valid_token_a(cls) -> list[str]:
        return ["valid_token_a"]

    @classmethod
    async def authenticate(cls, auth_token: str) -> None:
        if auth_token not in await cls.get_valid_token_c():
            raise AuthorizationOCPIError

    @classmethod
    async def authenticate_credentials(cls, auth_token: str) -> str | dict | None:
        if auth_token in await cls.get_valid_token_a():
            return {}
        if auth_token in await cls.get_valid_token_c():
            return auth_token
        return None


@pytest.mark.asyncio
async def test_authorization_verifier_valid_token_v2_1_1():
    """Test AuthorizationVerifier with valid token for OCPI 2.1.1."""
    verifier = AuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    # OCPI 2.1.1 doesn't require Base64 encoding
    result = await verifier("Token valid_token_c", authenticator)
    assert result is None  # authenticate doesn't return anything


@pytest.mark.asyncio
async def test_authorization_verifier_valid_token_v2_2_1():
    """Test AuthorizationVerifier with valid Base64 token for OCPI 2.2.1."""
    verifier = AuthorizationVerifier(VersionNumber.v_2_2_1)
    authenticator = MockAuthenticator()

    # OCPI 2.2.1 requires Base64 encoding
    from ocpi.core.utils import encode_string_base64

    encoded_token = encode_string_base64("valid_token_c")
    result = await verifier(f"Token {encoded_token}", authenticator)
    assert result is None


@pytest.mark.asyncio
async def test_authorization_verifier_invalid_token():
    """Test AuthorizationVerifier with invalid token raises AuthorizationOCPIError."""
    verifier = AuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    with pytest.raises(AuthorizationOCPIError):
        await verifier("Token invalid_token", authenticator)


@pytest.mark.asyncio
async def test_authorization_verifier_malformed_header():
    """Test AuthorizationVerifier with malformed header raises AuthorizationOCPIError."""
    verifier = AuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    with pytest.raises(AuthorizationOCPIError):
        await verifier("invalid", authenticator)


@pytest.mark.asyncio
async def test_authorization_verifier_no_auth():
    """Test AuthorizationVerifier with NO_AUTH setting."""
    verifier = AuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    with patch("ocpi.core.authentication.verifier.settings") as mock_settings:
        mock_settings.NO_AUTH = True
        result = await verifier("", authenticator)
        assert result is True


@pytest.mark.asyncio
async def test_credentials_authorization_verifier_token_a():
    """Test CredentialsAuthorizationVerifier with token A."""
    verifier = CredentialsAuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    result = await verifier("Token valid_token_a", authenticator)
    assert result == {}


@pytest.mark.asyncio
async def test_credentials_authorization_verifier_token_c():
    """Test CredentialsAuthorizationVerifier with token C."""
    verifier = CredentialsAuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    result = await verifier("Token valid_token_c", authenticator)
    assert result == "valid_token_c"


@pytest.mark.asyncio
async def test_credentials_authorization_verifier_invalid_token():
    """Test CredentialsAuthorizationVerifier with invalid token returns None."""
    verifier = CredentialsAuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    result = await verifier("Token invalid_token", authenticator)
    assert result is None


@pytest.mark.asyncio
async def test_credentials_authorization_verifier_base64_v2_2_1():
    """Test CredentialsAuthorizationVerifier with Base64 token for OCPI 2.2.1."""
    verifier = CredentialsAuthorizationVerifier(VersionNumber.v_2_2_1)
    authenticator = MockAuthenticator()

    from ocpi.core.utils import encode_string_base64

    encoded_token = encode_string_base64("valid_token_c")
    result = await verifier(f"Token {encoded_token}", authenticator)
    assert result == "valid_token_c"


@pytest.mark.asyncio
async def test_versions_authorization_verifier():
    """Test VersionsAuthorizationVerifier."""
    verifier = VersionsAuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    result = await verifier("Token valid_token_c", authenticator)
    assert result == "valid_token_c"


@pytest.mark.asyncio
async def test_versions_authorization_verifier_no_auth():
    """Test VersionsAuthorizationVerifier with NO_AUTH setting."""
    verifier = VersionsAuthorizationVerifier(VersionNumber.v_2_1_1)
    authenticator = MockAuthenticator()

    with patch("ocpi.core.authentication.verifier.settings") as mock_settings:
        mock_settings.NO_AUTH = True
        result = await verifier("", authenticator)
        assert result == ""


@pytest.mark.asyncio
async def test_http_push_verifier_valid_token():
    """Test HttpPushVerifier with valid token."""
    verifier = HttpPushVerifier()
    authenticator = MockAuthenticator()

    result = await verifier("Token valid_token_c", VersionNumber.v_2_1_1, authenticator)
    assert result is None


@pytest.mark.asyncio
async def test_http_push_verifier_base64_v2_3_0():
    """Test HttpPushVerifier with Base64 token for OCPI 2.3.0."""
    verifier = HttpPushVerifier()
    authenticator = MockAuthenticator()

    from ocpi.core.utils import encode_string_base64

    encoded_token = encode_string_base64("valid_token_c")
    result = await verifier(
        f"Token {encoded_token}", VersionNumber.v_2_3_0, authenticator
    )
    assert result is None


@pytest.mark.asyncio
async def test_http_push_verifier_invalid_token():
    """Test HttpPushVerifier with invalid token raises AuthorizationOCPIError."""
    verifier = HttpPushVerifier()
    authenticator = MockAuthenticator()

    with pytest.raises(AuthorizationOCPIError):
        await verifier("Token invalid_token", VersionNumber.v_2_1_1, authenticator)


@pytest.mark.asyncio
async def test_ws_push_verifier_valid_token():
    """Test WSPushVerifier with valid token."""
    verifier = WSPushVerifier()
    authenticator = MockAuthenticator()

    result = await verifier("valid_token_c", VersionNumber.v_2_1_1, authenticator)
    assert result is None


@pytest.mark.asyncio
async def test_ws_push_verifier_base64_v2_2_1():
    """Test WSPushVerifier with Base64 token for OCPI 2.2.1."""
    verifier = WSPushVerifier()
    authenticator = MockAuthenticator()

    from ocpi.core.utils import encode_string_base64

    encoded_token = encode_string_base64("valid_token_c")
    result = await verifier(encoded_token, VersionNumber.v_2_2_1, authenticator)
    assert result is None


@pytest.mark.asyncio
async def test_ws_push_verifier_empty_token():
    """Test WSPushVerifier with empty token raises WebSocketException."""
    verifier = WSPushVerifier()
    authenticator = MockAuthenticator()

    with pytest.raises(WebSocketException) as exc_info:
        await verifier("", VersionNumber.v_2_1_1, authenticator)
    assert exc_info.value.code == status.WS_1008_POLICY_VIOLATION


@pytest.mark.asyncio
async def test_ws_push_verifier_no_auth():
    """Test WSPushVerifier with NO_AUTH setting."""
    verifier = WSPushVerifier()
    authenticator = MockAuthenticator()

    with patch("ocpi.core.authentication.verifier.settings") as mock_settings:
        mock_settings.NO_AUTH = True
        result = await verifier("", VersionNumber.v_2_1_1, authenticator)
        assert result is True
