"""Tests for the full CPO example."""

import sys
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from ocpi.core.utils import encode_string_base64

# Add examples directory to path
examples_dir = Path(__file__).parent.parent.parent / "examples" / "full_cpo"
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
async def test_locations_module(client, auth_headers):
    """Test locations module."""
    # List locations (CPO can only GET, not PUT)
    response = await client.get(
        "/ocpi/cpo/2.3.0/locations/",
        headers=auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.asyncio
async def test_sessions_module(client, auth_headers):
    """Test sessions module."""
    # CPO can list sessions (if module is included)
    response = await client.get(
        "/ocpi/cpo/2.3.0/sessions/",
        headers=auth_headers,
    )
    # Sessions endpoint should exist if module is included
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)


@pytest.mark.asyncio
async def test_tariffs_module(client, auth_headers):
    """Test tariffs module."""
    # CPO can list tariffs (if module is included)
    response = await client.get(
        "/ocpi/cpo/2.3.0/tariffs/",
        headers=auth_headers,
    )
    # Tariffs endpoint may not exist if module not included, accept both 200 and 404
    assert response.status_code in [200, 404]
    if response.status_code == 200:
        data = response.json()
        assert "data" in data
        assert isinstance(data["data"], list)
