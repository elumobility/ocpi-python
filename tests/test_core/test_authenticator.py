"""Tests for ocpi.core.authentication.authenticator module."""

import pytest

from ocpi.core.authentication.authenticator import Authenticator
from ocpi.core.exceptions import AuthorizationOCPIError


class TestAuthenticator(Authenticator):
    """Test implementation of Authenticator."""

    @classmethod
    async def get_valid_token_c(cls) -> list[str]:
        """Return test valid token c list."""
        return ["valid_token_c_1", "valid_token_c_2"]

    @classmethod
    async def get_valid_token_a(cls) -> list[str]:
        """Return test valid token a list."""
        return ["valid_token_a_1", "valid_token_a_2"]


@pytest.mark.asyncio
async def test_authenticate_valid_token():
    """Test authenticate with valid token."""
    await TestAuthenticator.authenticate("valid_token_c_1")
    # Should not raise


@pytest.mark.asyncio
async def test_authenticate_invalid_token():
    """Test authenticate with invalid token raises AuthorizationOCPIError."""
    with pytest.raises(AuthorizationOCPIError):
        await TestAuthenticator.authenticate("invalid_token")


@pytest.mark.asyncio
async def test_authenticate_credentials_token_a():
    """Test authenticate_credentials with token A."""
    result = await TestAuthenticator.authenticate_credentials("valid_token_a_1")
    assert result == {}


@pytest.mark.asyncio
async def test_authenticate_credentials_token_c():
    """Test authenticate_credentials with token C."""
    result = await TestAuthenticator.authenticate_credentials("valid_token_c_1")
    assert result == "valid_token_c_1"


@pytest.mark.asyncio
async def test_authenticate_credentials_invalid_token():
    """Test authenticate_credentials with invalid token returns None."""
    result = await TestAuthenticator.authenticate_credentials("invalid_token")
    assert result is None


@pytest.mark.asyncio
async def test_authenticate_credentials_none():
    """Test authenticate_credentials with None returns None."""
    result = await TestAuthenticator.authenticate_credentials(None)
    assert result is None


@pytest.mark.asyncio
async def test_authenticate_credentials_empty_string():
    """Test authenticate_credentials with empty string."""
    result = await TestAuthenticator.authenticate_credentials("")
    assert result is None
