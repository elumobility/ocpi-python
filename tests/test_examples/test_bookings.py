# ruff: noqa: E402
"""Tests for the bookings example."""

import sys
from pathlib import Path

import pytest
from starlette.testclient import TestClient

# Add bookings example to path (conftest.py adds examples/ to path)
bookings_path = Path(__file__).parent.parent.parent / "examples" / "bookings"
bookings_path_str = str(bookings_path)
if bookings_path_str not in sys.path:
    sys.path.insert(0, bookings_path_str)

CPO_BASE_URL = "/ocpi/cpo/2.3.0/bookings"
# Base64-encoded token for OCPI 2.3.0 (my-cpo-token-123)
AUTH_HEADER = {"Authorization": "Token bXktY3BvLXRva2VuLTEyMw=="}


@pytest.fixture(scope="function")
def client():
    """Create test client with isolated storage."""
    # Import here to avoid module-level import issues
    # Use absolute import from bookings directory
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "examples" / "bookings"))
    try:
        import main  # noqa: E402
        import crud  # noqa: E402

        # Clear storage before each test
        crud.bookings_storage.clear()
        return TestClient(main.app)
    finally:
        # Clean up path
        if bookings_path_str in sys.path:
            sys.path.remove(bookings_path_str)


@pytest.fixture
def sample_booking():
    """Sample booking request data."""
    return {
        "emsp_booking_id": "EMSP-TEST-001",
        "token": {
            "country_code": "DE",
            "party_id": "EMS",
            "uid": "TEST-TOKEN-001",
            "type": "RFID",
            "contract_id": "DE-EMS-TEST001-1",
            "visual_number": "TEST001",
            "issuer": "Test EMSP",
            "group_id": None,
            "valid": True,
            "whitelist": "ALWAYS",
            "language": "de",
            "default_profile_type": None,
            "energy_contract": None,
            "last_updated": "2026-01-09T12:00:00Z",
        },
        "location_id": "LOC-TEST-001",
        "evse_uid": "EVSE-001",
        "connector_id": "CONN-001",
        "start_date_time": "2026-01-10T14:00:00Z",
        "end_date_time": "2026-01-10T16:00:00Z",
        "authorization_reference": "AUTH-TEST-001",
        "energy_estimate": 25.0,
    }


class TestBookingsExampleGet:
    """Test GET operations."""

    def test_get_bookings_list_empty(self, client):
        """Test getting bookings list (initially empty)."""
        response = client.get(CPO_BASE_URL, headers=AUTH_HEADER)
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000

    def test_get_booking_not_found(self, client):
        """Test getting a non-existent booking returns OCPI 2003."""
        response = client.get(f"{CPO_BASE_URL}/NONEXISTENT", headers=AUTH_HEADER)
        # OCPI returns 200 with status_code 2003 for unknown location
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 2003  # OCPI_2003_UNKNOWN_LOCATION


class TestBookingsExampleCreate:
    """Test POST operations."""

    def test_create_booking(self, client, sample_booking):
        """Test creating a new booking."""
        response = client.post(
            CPO_BASE_URL,
            json=sample_booking,
            headers=AUTH_HEADER,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
        assert "data" in data

        # Response contains a BookingResponse with result and booking
        booking_response = data["data"]
        assert booking_response["result"] == "ACCEPTED"
        assert "booking" in booking_response

        booking = booking_response["booking"]
        # CiString lowercases values per OCPI spec
        assert booking["location_id"].lower() == "loc-test-001"
        assert booking["state"] == "CONFIRMED"
        assert booking["emsp_booking_id"].lower() == "emsp-test-001"


class TestBookingsExampleUpdate:
    """Test PATCH operations."""

    def test_update_booking(self, client, sample_booking):
        """Test updating a booking."""
        # First create a booking
        create_response = client.post(
            CPO_BASE_URL,
            json=sample_booking,
            headers=AUTH_HEADER,
        )
        assert create_response.status_code == 200
        booking_id = create_response.json()["data"]["booking"]["id"]

        # Now update it
        update_data = {"state": "ACTIVE"}
        response = client.patch(
            f"{CPO_BASE_URL}/{booking_id}",
            json=update_data,
            headers=AUTH_HEADER,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
        assert data["data"]["state"] == "ACTIVE"


class TestBookingsExampleDelete:
    """Test DELETE operations."""

    def test_cancel_booking(self, client, sample_booking):
        """Test cancelling a booking."""
        # First create a booking
        create_response = client.post(
            CPO_BASE_URL,
            json=sample_booking,
            headers=AUTH_HEADER,
        )
        assert create_response.status_code == 200
        booking_id = create_response.json()["data"]["booking"]["id"]

        # Now cancel it
        response = client.delete(
            f"{CPO_BASE_URL}/{booking_id}",
            headers=AUTH_HEADER,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000


class TestBookingsExampleAuth:
    """Test authentication."""

    def test_unauthorized_without_token(self, client):
        """Test that requests without token are rejected."""
        response = client.get(CPO_BASE_URL)
        # OCPI returns 403 Forbidden for auth failures
        assert response.status_code == 403

    def test_unauthorized_with_invalid_token(self, client):
        """Test that requests with invalid token are rejected."""
        response = client.get(
            CPO_BASE_URL,
            headers={
                "Authorization": "Token aW52YWxpZC10b2tlbg=="
            },  # Base64 of "invalid-token"
        )
        assert response.status_code == 403
