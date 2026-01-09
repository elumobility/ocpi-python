"""Tests for OCPI 2.3.0 Bookings CPO API."""

from datetime import UTC, datetime, timedelta

import pytest
from fastapi.testclient import TestClient

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.bookings.v_2_3_0.enums import BookingResponseType, BookingState
from ocpi.modules.versions.enums import VersionNumber
from tests.test_modules.test_v_2_3_0.test_bookings.utils import (
    ADAPTER,
    BOOKING_ID,
    ClientAuthenticator,
    Crud,
)
from tests.test_modules.utils import ENCODED_AUTH_TOKEN_V_2_3_0

CPO_BASE_URL = "/ocpi/cpo/2.3.0"


@pytest.fixture
def client():
    """Create test client for CPO bookings API."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[RoleEnum.cpo],
        modules=[ModuleID.bookings],
        authenticator=ClientAuthenticator,
        crud=Crud,
        adapter=ADAPTER,
    )
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create authorization headers with Base64 encoded token."""
    return {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}


class TestCPOBookingsGet:
    """Tests for GET /bookings endpoints."""

    def test_get_bookings_list(self, client, auth_headers):
        """Test getting list of bookings."""
        response = client.get(f"{CPO_BASE_URL}/bookings", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
        assert isinstance(data["data"], list)

    def test_get_booking_by_id(self, client, auth_headers):
        """Test getting a specific booking by ID."""
        response = client.get(
            f"{CPO_BASE_URL}/bookings/{BOOKING_ID}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
        # Check that we got a booking data object
        assert "id" in data["data"]

    def test_get_booking_not_found(self, client, auth_headers):
        """Test getting a non-existent booking."""
        response = client.get(
            f"{CPO_BASE_URL}/bookings/NONEXISTENT",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 2003  # Unknown location
        assert data["data"] == []


class TestCPOBookingsCreate:
    """Tests for POST /bookings endpoint."""

    def test_create_booking(self, client, auth_headers):
        """Test creating a new booking."""
        booking_request = {
            "emsp_booking_id": "EMSP-NEW-001",
            "token": {
                "country_code": "DE",
                "party_id": "ELU",
                "uid": "TOKEN-NEW",
                "type": "RFID",
                "contract_id": "CONTRACT-NEW",
                "visual_number": "99999999",
                "issuer": "ELU Mobility",
                "group_id": None,
                "valid": True,
                "whitelist": "ALWAYS",
                "language": None,
                "default_profile_type": None,
                "energy_contract": None,
                "last_updated": datetime.now(UTC).isoformat(),
            },
            "location_id": "LOC-001",
            "evse_uid": "EVSE-001",
            "start_date_time": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
            "end_date_time": (datetime.now(UTC) + timedelta(hours=4)).isoformat(),
        }

        response = client.post(
            f"{CPO_BASE_URL}/bookings",
            json=booking_request,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
        assert data["data"]["result"] == BookingResponseType.accepted


class TestCPOBookingsUpdate:
    """Tests for PATCH /bookings/{booking_id} endpoint."""

    def test_update_booking(self, client, auth_headers):
        """Test partially updating a booking."""
        update_data = {"state": BookingState.active}

        response = client.patch(
            f"{CPO_BASE_URL}/bookings/{BOOKING_ID}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000


class TestCPOBookingsDelete:
    """Tests for DELETE /bookings/{booking_id} endpoint."""

    def test_cancel_booking(self, client, auth_headers):
        """Test cancelling a booking."""
        response = client.delete(
            f"{CPO_BASE_URL}/bookings/{BOOKING_ID}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
