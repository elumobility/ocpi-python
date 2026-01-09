"""Tests for ocpi.core.push module."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from ocpi.core import enums, schemas
from ocpi.core.adapter import BaseAdapter
from ocpi.core.crud import Crud
from ocpi.core.push import (
    client_method,
    client_url,
    push_object,
    request_data,
    send_push_request,
)
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.v_2_2_1.enums import InterfaceRole


class MockCrud(Crud):
    @classmethod
    async def get(cls, module, role, id, *args, **kwargs):
        return {"id": id, "data": "test"}

    @classmethod
    async def list(cls, module, role, filters, *args, **kwargs):
        return [], 0, False

    @classmethod
    async def create(cls, module, role, data, *args, **kwargs):
        return data

    @classmethod
    async def update(cls, module, role, id, data, *args, **kwargs):
        return data

    @classmethod
    async def delete(cls, module, role, id, *args, **kwargs):
        return None

    @classmethod
    async def do(cls, module, role, action, *args, **kwargs):
        return None


class MockAdapter(BaseAdapter):
    def location_adapter(self, data, version):
        mock_location = MagicMock()
        mock_location.model_dump.return_value = data
        return mock_location

    def session_adapter(self, data, version):
        mock_session = MagicMock()
        mock_session.model_dump.return_value = data
        return mock_session

    def cdr_adapter(self, data, version):
        mock_cdr = MagicMock()
        mock_cdr.model_dump.return_value = data
        return mock_cdr

    def tariff_adapter(self, data, version):
        mock_tariff = MagicMock()
        mock_tariff.model_dump.return_value = data
        return mock_tariff

    def token_adapter(self, data, version):
        mock_token = MagicMock()
        mock_token.model_dump.return_value = data
        return mock_token


def test_client_url_cdrs():
    """Test client_url for CDRs module."""
    base_url = "https://example.com"
    url = client_url(enums.ModuleID.cdrs, "cdr-123", base_url)
    assert url == base_url


def test_client_url_non_cdrs():
    """Test client_url for non-CDRs modules."""
    base_url = "https://example.com"
    url = client_url(enums.ModuleID.locations, "loc-123", base_url)
    assert "loc-123" in url
    assert base_url in url


def test_client_method_cdrs():
    """Test client_method for CDRs module."""
    method = client_method(enums.ModuleID.cdrs)
    assert method == "POST"


def test_client_method_non_cdrs():
    """Test client_method for non-CDRs modules."""
    method = client_method(enums.ModuleID.locations)
    assert method == "PUT"


def test_request_data_locations():
    """Test request_data for locations module."""
    adapter = MockAdapter()
    data = {"id": "loc-123", "name": "Test Location"}
    result = request_data(
        enums.ModuleID.locations, data, adapter, VersionNumber.v_2_2_1
    )
    assert result is not None
    assert "id" in result


def test_request_data_sessions():
    """Test request_data for sessions module."""
    adapter = MockAdapter()
    data = {"id": "sess-123", "status": "ACTIVE"}
    result = request_data(enums.ModuleID.sessions, data, adapter, VersionNumber.v_2_2_1)
    assert result is not None


def test_request_data_cdrs():
    """Test request_data for CDRs module."""
    adapter = MockAdapter()
    data = {"id": "cdr-123", "currency": "EUR"}
    result = request_data(enums.ModuleID.cdrs, data, adapter, VersionNumber.v_2_2_1)
    assert result is not None


def test_request_data_tariffs():
    """Test request_data for tariffs module."""
    adapter = MockAdapter()
    data = {"id": "tariff-123", "currency": "EUR"}
    result = request_data(enums.ModuleID.tariffs, data, adapter, VersionNumber.v_2_2_1)
    assert result is not None


def test_request_data_tokens():
    """Test request_data for tokens module."""
    adapter = MockAdapter()
    data = {"uid": "token-123", "type": "RFID"}
    result = request_data(enums.ModuleID.tokens, data, adapter, VersionNumber.v_2_2_1)
    assert result is not None


@pytest.mark.asyncio
async def test_send_push_request_v2_1_1():
    """Test send_push_request for OCPI 2.1.1."""
    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.location_adapter.return_value.model_dump.return_value = {
        "id": "loc-123"
    }

    endpoints = [{"identifier": enums.ModuleID.locations, "url": "https://example.com"}]

    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        response = await send_push_request(
            object_id="loc-123",
            object_data={"id": "loc-123"},
            module_id=enums.ModuleID.locations,
            adapter=mock_adapter,
            client_auth_token="Token test-token",
            endpoints=endpoints,
            version=VersionNumber.v_2_1_1,
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_send_push_request_v2_2_1():
    """Test send_push_request for OCPI 2.2.1 with receiver role."""
    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.location_adapter.return_value.model_dump.return_value = {
        "id": "loc-123"
    }

    endpoints = [
        {
            "identifier": enums.ModuleID.locations,
            "role": InterfaceRole.receiver,
            "url": "https://example.com",
        }
    ]

    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        response = await send_push_request(
            object_id="loc-123",
            object_data={"id": "loc-123"},
            module_id=enums.ModuleID.locations,
            adapter=mock_adapter,
            client_auth_token="Token test-token",
            endpoints=endpoints,
            version=VersionNumber.v_2_2_1,
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_push_object_tokens_module():
    """Test push_object with tokens module (uses EMSP role)."""
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.get.return_value = {"uid": "token-123", "type": "RFID"}

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.token_adapter.return_value.model_dump.return_value = {
        "uid": "token-123"
    }

    push = schemas.Push(
        module_id=enums.ModuleID.tokens,
        object_id="token-123",
        receivers=[
            schemas.Receiver(
                endpoints_url="https://example.com/versions", auth_token="token"
            ),
        ],
    )

    # Mock endpoints response
    mock_endpoints_response = MagicMock()
    mock_endpoints_response.status_code = 200
    mock_endpoints_response.json.return_value = {
        "data": {
            "endpoints": [
                {
                    "identifier": enums.ModuleID.tokens,
                    "url": "https://example.com/tokens",
                }
            ]
        }
    }

    # Mock push request response
    mock_push_response = MagicMock()
    mock_push_response.status_code = 200
    mock_push_response.json.return_value = {"status_code": 1000}

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        result = await push_object(
            version=VersionNumber.v_2_1_1,
            push=push,
            crud=mock_crud,
            adapter=mock_adapter,
            auth_token="auth-token",
        )

    assert len(result.receiver_responses) == 1
    assert result.receiver_responses[0].status_code == 200
    # Should use EMSP role for tokens
    mock_crud.get.assert_awaited_with(
        enums.ModuleID.tokens,
        enums.RoleEnum.emsp,
        "token-123",
        auth_token="auth-token",
        version=VersionNumber.v_2_1_1,
    )


@pytest.mark.asyncio
async def test_push_object_cdrs_module():
    """Test push_object with CDRs module (special response handling)."""
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.get.return_value = {"id": "cdr-123", "currency": "EUR"}

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.cdr_adapter.return_value.model_dump.return_value = {"id": "cdr-123"}

    push = schemas.Push(
        module_id=enums.ModuleID.cdrs,
        object_id="cdr-123",
        receivers=[
            schemas.Receiver(
                endpoints_url="https://example.com/versions", auth_token="token"
            ),
        ],
    )

    # Mock endpoints response
    mock_endpoints_response = MagicMock()
    mock_endpoints_response.status_code = 200
    mock_endpoints_response.json.return_value = {
        "data": {
            "endpoints": [
                {
                    "identifier": enums.ModuleID.cdrs,
                    "url": "https://example.com/cdrs",
                }
            ]
        }
    }

    # Mock push request response with headers
    mock_push_response = MagicMock()
    mock_push_response.status_code = 200
    mock_push_response.headers = {"X-Request-ID": "req-123"}

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        result = await push_object(
            version=VersionNumber.v_2_1_1,
            push=push,
            crud=mock_crud,
            adapter=mock_adapter,
            auth_token="auth-token",
        )

    assert len(result.receiver_responses) == 1
    assert result.receiver_responses[0].status_code == 200
    # CDR response should contain headers, not JSON
    assert result.receiver_responses[0].response == {"X-Request-ID": "req-123"}


@pytest.mark.asyncio
async def test_push_object_v2_1_1_token_encoding():
    """Test push_object with OCPI 2.1.1 (no Base64 encoding)."""
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.get.return_value = {"id": "loc-123"}

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.location_adapter.return_value.model_dump.return_value = {
        "id": "loc-123"
    }

    push = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="loc-123",
        receivers=[
            schemas.Receiver(
                endpoints_url="https://example.com/versions", auth_token="raw-token"
            ),
        ],
    )

    # Mock endpoints response
    mock_endpoints_response = MagicMock()
    mock_endpoints_response.status_code = 200
    mock_endpoints_response.json.return_value = {
        "data": {
            "endpoints": [
                {
                    "identifier": enums.ModuleID.locations,
                    "url": "https://example.com/locations",
                }
            ]
        }
    }

    # Mock push request response
    mock_push_response = MagicMock()
    mock_push_response.status_code = 200
    mock_push_response.json.return_value = {"status_code": 1000}

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        await push_object(
            version=VersionNumber.v_2_1_1,
            push=push,
            crud=mock_crud,
            adapter=mock_adapter,
            auth_token="auth-token",
        )

    # Verify token was not Base64 encoded (2.1.1 uses raw tokens)
    # The build_request should have been called with raw token
    mock_client.return_value.__aenter__.return_value.build_request.assert_called()
    call_args = mock_client.return_value.__aenter__.return_value.build_request.call_args
    assert "Token raw-token" in str(call_args)


@pytest.mark.asyncio
async def test_push_object_v2_2_1_token_encoding():
    """Test push_object with OCPI 2.2.1 (Base64 encoding)."""
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.get.return_value = {"id": "loc-123"}

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.location_adapter.return_value.model_dump.return_value = {
        "id": "loc-123"
    }

    push = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="loc-123",
        receivers=[
            schemas.Receiver(
                endpoints_url="https://example.com/versions", auth_token="raw-token"
            ),
        ],
    )

    # Mock endpoints response
    mock_endpoints_response = MagicMock()
    mock_endpoints_response.status_code = 200
    mock_endpoints_response.json.return_value = {
        "data": {
            "endpoints": [
                {
                    "identifier": enums.ModuleID.locations,
                    "role": InterfaceRole.receiver,
                    "url": "https://example.com/locations",
                }
            ]
        }
    }

    # Mock push request response
    mock_push_response = MagicMock()
    mock_push_response.status_code = 200
    mock_push_response.json.return_value = {"status_code": 1000}

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        await push_object(
            version=VersionNumber.v_2_2_1,
            push=push,
            crud=mock_crud,
            adapter=mock_adapter,
            auth_token="auth-token",
        )

    # Verify token was Base64 encoded (2.2.1 uses Base64)
    mock_client.return_value.__aenter__.return_value.build_request.assert_called()
    call_args = mock_client.return_value.__aenter__.return_value.build_request.call_args
    # Should contain Base64 encoded token
    assert "Token" in str(call_args)


@pytest.mark.asyncio
async def test_push_object_multiple_receivers():
    """Test push_object with multiple receivers."""
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.get.return_value = {"id": "loc-123"}

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.location_adapter.return_value.model_dump.return_value = {
        "id": "loc-123"
    }

    push = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="loc-123",
        receivers=[
            schemas.Receiver(
                endpoints_url="https://example1.com/versions", auth_token="token1"
            ),
            schemas.Receiver(
                endpoints_url="https://example2.com/versions", auth_token="token2"
            ),
        ],
    )

    # Mock endpoints response
    mock_endpoints_response = MagicMock()
    mock_endpoints_response.status_code = 200
    mock_endpoints_response.json.return_value = {
        "data": {
            "endpoints": [
                {
                    "identifier": enums.ModuleID.locations,
                    "url": "https://example.com/locations",
                }
            ]
        }
    }

    # Mock push request response
    mock_push_response = MagicMock()
    mock_push_response.status_code = 200
    mock_push_response.json.return_value = {"status_code": 1000}

    with patch("ocpi.core.push.httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_endpoints_response
        )
        mock_client.return_value.__aenter__.return_value.send = AsyncMock(
            return_value=mock_push_response
        )
        mock_client.return_value.__aenter__.return_value.build_request = MagicMock()

        result = await push_object(
            version=VersionNumber.v_2_1_1,
            push=push,
            crud=mock_crud,
            adapter=mock_adapter,
            auth_token="auth-token",
        )

    # Should have responses for both receivers
    assert len(result.receiver_responses) == 2
    assert mock_client.return_value.__aenter__.return_value.get.await_count == 2
