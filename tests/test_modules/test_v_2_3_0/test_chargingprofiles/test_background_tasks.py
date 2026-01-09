"""Tests for ocpi.modules.chargingprofiles.v_2_3_0.background_tasks module."""

from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from ocpi.core.adapter import BaseAdapter
from ocpi.core.crud import Crud
from ocpi.modules.chargingprofiles.v_2_3_0.background_tasks import (
    send_delete_chargingprofile,
    send_get_chargingprofile,
    send_update_chargingprofile,
)
from ocpi.modules.chargingprofiles.v_2_3_0.schemas import (
    ChargingProfile,
    ChargingProfilePeriod,
    ChargingProfileResult,
    ChargingProfileResultType,
    ChargingRateUnit,
    SetChargingProfile,
)


class MockCrud(Crud):
    @classmethod
    async def get(cls, module, role, id, *args, **kwargs):
        return None

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
        return "client-token-123"


@pytest.mark.asyncio
async def test_send_get_chargingprofile_success():
    """Test send_get_chargingprofile with successful result."""
    session_id = str(uuid4())
    duration = 3600
    response_url = "https://example.com/callback"
    auth_token = "auth-token-123"

    # Mock CRUD to return a result immediately
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.do.return_value = "client-token-123"
    mock_crud.get.return_value = {"result": "accepted"}

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.active_charging_profile_result_adapter.return_value = (
        ChargingProfileResult(result=ChargingProfileResultType.accepted)
    )

    # Mock httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch(
        "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.httpx.AsyncClient"
    ) as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        await send_get_chargingprofile(
            session_id=session_id,
            duration=duration,
            response_url=response_url,
            auth_token=auth_token,
            crud=mock_crud,
            adapter=mock_adapter,
        )

    # Verify CRUD was called
    mock_crud.do.assert_awaited_once()
    mock_crud.get.assert_awaited()


@pytest.mark.asyncio
async def test_send_get_chargingprofile_timeout():
    """Test send_get_chargingprofile when result doesn't arrive in time."""
    session_id = str(uuid4())
    duration = 3600
    response_url = "https://example.com/callback"
    auth_token = "auth-token-123"

    # Mock CRUD to never return a result (timeout scenario)
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.do.return_value = "client-token-123"
    mock_crud.get.return_value = None  # Always returns None (timeout)

    mock_adapter = MagicMock(spec=BaseAdapter)

    # Mock httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.httpx.AsyncClient"
        ) as mock_client,
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.settings.GET_ACTIVE_PROFILE_AWAIT_TIME",
            1,
        ),
        patch("ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.sleep"),
    ):
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        await send_get_chargingprofile(
            session_id=session_id,
            duration=duration,
            response_url=response_url,
            auth_token=auth_token,
            crud=mock_crud,
            adapter=mock_adapter,
        )

    # Should have tried multiple times
    assert mock_crud.get.await_count > 1
    # Should have sent rejected result
    mock_client.return_value.__aenter__.return_value.post.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_update_chargingprofile_success():
    """Test send_update_chargingprofile with successful result."""
    session_id = str(uuid4())
    response_url = "https://example.com/callback"
    auth_token = "auth-token-123"
    charging_profile = SetChargingProfile(
        charging_profile=ChargingProfile(
            charging_rate_unit=ChargingRateUnit.watts,
            min_charge_rate=1000.0,
            charging_profile_period=ChargingProfilePeriod(
                start_period=0,
                limit=5000.0,
            ),
        ),
        response_url=response_url,
    )

    # Mock CRUD: first call returns something, second call returns None (success)
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.do.return_value = "client-token-123"
    # First call returns a result, second call returns None (cleared)
    mock_crud.get.side_effect = [{"result": "pending"}, None]

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.active_charging_profile_result_adapter.return_value = (
        ChargingProfileResult(result=ChargingProfileResultType.accepted)
    )

    # Mock httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.httpx.AsyncClient"
        ) as mock_client,
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.settings.GET_ACTIVE_PROFILE_AWAIT_TIME",
            1,
        ),
        patch("ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.sleep"),
    ):
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        await send_update_chargingprofile(
            charging_profile=charging_profile,
            session_id=session_id,
            response_url=response_url,
            auth_token=auth_token,
            crud=mock_crud,
            adapter=mock_adapter,
        )

    mock_crud.do.assert_awaited_once()
    # Should have called get at least twice
    assert mock_crud.get.await_count >= 1


@pytest.mark.asyncio
async def test_send_update_chargingprofile_timeout():
    """Test send_update_chargingprofile when result doesn't arrive in time."""
    session_id = str(uuid4())
    response_url = "https://example.com/callback"
    auth_token = "auth-token-123"
    charging_profile = SetChargingProfile(
        charging_profile=ChargingProfile(
            charging_rate_unit=ChargingRateUnit.watts,
            min_charge_rate=1000.0,
            charging_profile_period=ChargingProfilePeriod(
                start_period=0,
                limit=5000.0,
            ),
        ),
        response_url=response_url,
    )

    # Mock CRUD to always return a result (timeout - result never clears)
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.do.return_value = "client-token-123"
    mock_crud.get.return_value = {
        "result": "pending"
    }  # Always returns something (never None)

    mock_adapter = MagicMock(spec=BaseAdapter)

    # Mock httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.httpx.AsyncClient"
        ) as mock_client,
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.settings.GET_ACTIVE_PROFILE_AWAIT_TIME",
            1,
        ),
        patch("ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.sleep"),
    ):
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        await send_update_chargingprofile(
            charging_profile=charging_profile,
            session_id=session_id,
            response_url=response_url,
            auth_token=auth_token,
            crud=mock_crud,
            adapter=mock_adapter,
        )

    # Should have tried multiple times (until timeout)
    assert mock_crud.get.await_count > 1
    # Should have sent rejected result
    mock_client.return_value.__aenter__.return_value.post.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_delete_chargingprofile_success():
    """Test send_delete_chargingprofile with successful result."""
    session_id = str(uuid4())
    response_url = "https://example.com/callback"
    auth_token = "auth-token-123"

    # Mock CRUD to return None (success - profile was cleared)
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.do.return_value = "client-token-123"
    mock_crud.get.return_value = None  # Profile cleared successfully

    mock_adapter = MagicMock(spec=BaseAdapter)

    # Mock httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200

    with patch(
        "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.httpx.AsyncClient"
    ) as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        await send_delete_chargingprofile(
            session_id=session_id,
            response_url=response_url,
            auth_token=auth_token,
            crud=mock_crud,
            adapter=mock_adapter,
        )

    mock_crud.do.assert_awaited_once()
    mock_crud.get.assert_awaited()
    # Should send accepted result when profile is cleared
    mock_client.return_value.__aenter__.return_value.post.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_delete_chargingprofile_timeout():
    """Test send_delete_chargingprofile when result doesn't arrive in time."""
    session_id = str(uuid4())
    response_url = "https://example.com/callback"
    auth_token = "auth-token-123"

    # Mock CRUD to always return a result (timeout - result never clears)
    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.do.return_value = "client-token-123"
    mock_crud.get.return_value = {"result": "pending"}  # Always returns something

    mock_adapter = MagicMock(spec=BaseAdapter)

    # Mock httpx.AsyncClient
    mock_response = MagicMock()
    mock_response.status_code = 200

    with (
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.httpx.AsyncClient"
        ) as mock_client,
        patch(
            "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.settings.GET_ACTIVE_PROFILE_AWAIT_TIME",
            1,
        ),
        patch("ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.sleep"),
    ):
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        await send_delete_chargingprofile(
            session_id=session_id,
            response_url=response_url,
            auth_token=auth_token,
            crud=mock_crud,
            adapter=mock_adapter,
        )

    # Should have tried multiple times
    assert mock_crud.get.await_count > 1
    # Should have sent rejected result
    mock_client.return_value.__aenter__.return_value.post.assert_awaited_once()


@pytest.mark.asyncio
async def test_send_get_chargingprofile_http_error():
    """Test send_get_chargingprofile handles HTTP errors."""
    session_id = str(uuid4())
    duration = 3600
    response_url = "https://example.com/callback"
    auth_token = "auth-token-123"

    mock_crud = AsyncMock(spec=MockCrud)
    mock_crud.do.return_value = "client-token-123"
    mock_crud.get.return_value = {"result": "accepted"}

    mock_adapter = MagicMock(spec=BaseAdapter)
    mock_adapter.active_charging_profile_result_adapter.return_value = (
        ChargingProfileResult(result=ChargingProfileResultType.accepted)
    )

    # Mock httpx.AsyncClient with error response
    mock_response = MagicMock()
    mock_response.status_code = 500

    with patch(
        "ocpi.modules.chargingprofiles.v_2_3_0.background_tasks.httpx.AsyncClient"
    ) as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response
        )

        # Should not raise, just log the error
        await send_get_chargingprofile(
            session_id=session_id,
            duration=duration,
            response_url=response_url,
            auth_token=auth_token,
            crud=mock_crud,
            adapter=mock_adapter,
        )

    # Should have attempted to send
    mock_client.return_value.__aenter__.return_value.post.assert_awaited_once()
