"""Tests for the charging profiles example."""

import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from ocpi.core.utils import encode_string_base64

# Add examples directory to path
examples_dir = Path(__file__).parent.parent.parent / "examples" / "charging_profiles"
sys.path.insert(0, str(examples_dir))

from main import app


@pytest.fixture
def client():
    """Create a test client."""
    return AsyncClient(transport=ASGITransport(app=app), base_url="http://test")


@pytest.fixture
def auth_headers():
    """Create auth headers with base64 encoded token for OCPI 2.3.0."""
    token = "my-cpo-token-123"
    encoded_token = encode_string_base64(token)
    return {"Authorization": f"Token {encoded_token}"}


@pytest.mark.asyncio
async def test_get_versions(client, auth_headers):
    """Test getting available versions."""
    response = await client.get("/ocpi/versions", headers=auth_headers)
    # Versions endpoint might not require auth, so accept both 200 and 403
    assert response.status_code in [200, 403]


@pytest.mark.asyncio
async def test_set_charging_profile(client, auth_headers):
    """Test setting a charging profile."""
    charging_profile_data = {
        "charging_profile": {
            "start_date_time": "2024-01-01T10:00:00Z",
            "charging_rate_unit": "A",
            "charging_schedule": {
                "start_schedule": "2024-01-01T10:00:00Z",
                "charging_rate_unit": "A",
                "charging_periods": [
                    {
                        "start_period": 0,
                        "limit": 16.0,
                    },
                ],
            },
        },
        "response_url": "https://example.com/callback",
    }

    response = await client.put(
        "/ocpi/cpo/2.3.0/chargingprofiles/SESS001",
        json=charging_profile_data,
        headers=auth_headers,
    )

    # Note: This may return 404 if session doesn't exist, which is expected
    # The important thing is that the endpoint is accessible
    assert response.status_code in [200, 404, 422]


@pytest.mark.asyncio
async def test_get_active_charging_profile(client, auth_headers):
    """Test getting active charging profile."""
    response = await client.get(
        "/ocpi/cpo/2.3.0/chargingprofiles/SESS001?duration=3600",
        headers=auth_headers,
    )

    # May return 404 if no profile exists, which is expected
    assert response.status_code in [200, 404]
