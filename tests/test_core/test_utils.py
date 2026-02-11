"""Tests for ocpi.core.utils module."""

import pytest
from fastapi import Request, Response
from pydantic import BaseModel

from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.utils import (
    decode_string_base64,
    encode_string_base64,
    get_auth_token,
    get_list,
    get_module_model,
    partially_update_attributes,
    set_pagination_headers,
)
from ocpi.modules.versions.enums import VersionNumber


def test_set_pagination_headers():
    """Test set_pagination_headers sets correct headers."""
    response = Response()
    link = '<https://example.com>; rel="next"'
    total = 100
    limit = 50

    result = set_pagination_headers(response, link, total, limit)

    assert result.headers["Link"] == link
    assert result.headers["X-Total-Count"] == "100"
    assert result.headers["X-Limit"] == "50"


def test_get_auth_token_v2_1_1():
    """Test get_auth_token with OCPI 2.1.1 (no Base64 encoding)."""
    from unittest.mock import MagicMock

    # Create a mock request with headers
    request = MagicMock(spec=Request)
    request.headers = {"authorization": "Token test-token-123"}

    token = get_auth_token(request, VersionNumber.v_2_1_1)
    assert token == "test-token-123"


def test_get_auth_token_v2_2_1_base64():
    """Test get_auth_token with OCPI 2.2.1 (Base64 encoding)."""
    from unittest.mock import MagicMock

    original_token = "test-token-123"
    encoded_token = encode_string_base64(original_token)

    # Create a mock request with headers
    request = MagicMock(spec=Request)
    request.headers = {"authorization": f"Token {encoded_token}"}

    token = get_auth_token(request, VersionNumber.v_2_2_1)
    assert token == original_token


def test_get_auth_token_v2_2_1_plain_text_fallback():
    """Test get_auth_token with OCPI 2.2.1 falls back to raw token when base64 decode fails."""
    from unittest.mock import MagicMock

    # Plain-text token (not base64) - e.g. dev token
    raw_token = "plain-dev-token"

    request = MagicMock(spec=Request)
    request.headers = {"authorization": f"Token {raw_token}"}

    token = get_auth_token(request, VersionNumber.v_2_2_1)
    assert token == raw_token


def test_get_auth_token_null():
    """Test get_auth_token with Null token returns None."""
    from unittest.mock import MagicMock

    # Create a mock request with headers
    request = MagicMock(spec=Request)
    request.headers = {"authorization": "Token Null"}

    token = get_auth_token(request, VersionNumber.v_2_1_1)
    assert token is None


def test_get_auth_token_websocket():
    """Test get_auth_token with WebSocket."""

    # Create a mock WebSocket
    class MockWebSocket:
        def __init__(self):
            self.headers = {"authorization": "Token test-token-123"}

    ws = MockWebSocket()
    token = get_auth_token(ws, VersionNumber.v_2_1_1)  # type: ignore
    assert token == "test-token-123"


@pytest.mark.asyncio
async def test_get_list_with_pagination():
    """Test get_list with pagination (not last page)."""

    class MockCrud:
        @classmethod
        async def list(cls, module, role, filters, *args, **kwargs):
            return [{"id": "1"}, {"id": "2"}], 10, False  # has_more = False

    response = Response()
    filters = {"offset": 0, "limit": 2}

    result = await get_list(
        response,
        filters,
        ModuleID.locations,
        RoleEnum.cpo,
        VersionNumber.v_2_3_0,
        MockCrud,
    )

    assert len(result) == 2
    assert "Link" in response.headers
    assert response.headers["X-Total-Count"] == "10"
    assert response.headers["X-Limit"] == "2"


@pytest.mark.asyncio
async def test_get_list_last_page():
    """Test get_list when it's the last page (no Link header)."""

    class MockCrud:
        @classmethod
        async def list(cls, module, role, filters, *args, **kwargs):
            return [{"id": "1"}], 1, True  # has_more = True (last page)

    response = Response()
    filters = {"offset": 0, "limit": 2}

    result = await get_list(
        response,
        filters,
        ModuleID.locations,
        RoleEnum.cpo,
        VersionNumber.v_2_3_0,
        MockCrud,
    )

    assert len(result) == 1
    assert response.headers["Link"] == ""  # No next page link
    assert response.headers["X-Total-Count"] == "1"


def test_partially_update_attributes():
    """Test partially_update_attributes updates model attributes."""

    class TestModel(BaseModel):
        name: str = "original"
        value: int = 0

    instance = TestModel()
    partially_update_attributes(instance, {"name": "updated", "value": 42})

    assert instance.name == "updated"
    assert instance.value == 42


def test_encode_string_base64():
    """Test encode_string_base64 encodes string correctly."""
    original = "test-string"
    encoded = encode_string_base64(original)

    assert encoded != original
    assert isinstance(encoded, str)
    # Verify it can be decoded back
    decoded = decode_string_base64(encoded)
    assert decoded == original


def test_decode_string_base64():
    """Test decode_string_base64 decodes string correctly."""
    original = "test-string"
    encoded = encode_string_base64(original)
    decoded = decode_string_base64(encoded)

    assert decoded == original


def test_get_module_model_valid():
    """Test get_module_model with valid module and class."""
    Location = get_module_model("Location", "locations", "v_2_3_0")
    assert Location is not None
    # Verify it's a Pydantic model
    assert hasattr(Location, "model_validate")


def test_get_module_model_invalid_module():
    """Test get_module_model with invalid module raises NotImplementedError."""
    with pytest.raises(NotImplementedError) as exc_info:
        get_module_model("Location", "nonexistent", "v_2_3_0")

    assert "not found" in str(exc_info.value).lower()


def test_get_module_model_invalid_class():
    """Test get_module_model with invalid class name raises AttributeError."""
    with pytest.raises(AttributeError):
        get_module_model("NonExistentClass", "locations", "v_2_3_0")
