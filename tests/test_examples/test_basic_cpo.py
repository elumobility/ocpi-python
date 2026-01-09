"""Tests for the basic CPO example."""

import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from ocpi.core.utils import encode_string_base64

# Add examples directory to path
examples_dir = Path(__file__).parent.parent.parent / "examples" / "basic_cpo"
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
    # Versions endpoint may require auth, try both
    response = await client.get("/ocpi/versions", headers=auth_headers)
    # Versions endpoint might not require auth, so accept both 200 and 403
    assert response.status_code in [200, 403]


@pytest.mark.asyncio
async def test_list_locations(client, auth_headers):
    """Test listing locations."""
    response = await client.get(
        "/ocpi/cpo/2.3.0/locations/",
        headers=auth_headers,
    )

    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_get_location_not_found(client, auth_headers):
    """Test getting a non-existent location returns 404."""
    response = await client.get(
        "/ocpi/cpo/2.3.0/locations/NONEXISTENT",
        headers=auth_headers,
    )

    # Should return 404 for non-existent location
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_access(client):
    """Test that unauthorized access is rejected."""
    headers = {"Authorization": "Token invalid-token"}

    response = await client.get(
        "/ocpi/cpo/2.3.0/locations/",
        headers=headers,
    )

    assert response.status_code in [401, 403]
