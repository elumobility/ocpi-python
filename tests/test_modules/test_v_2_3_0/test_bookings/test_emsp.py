"""Tests for OCPI 2.3.0 Bookings EMSP API."""

from datetime import UTC, datetime

import pytest
from fastapi.testclient import TestClient

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.bookings.v_2_3_0.enums import BookingState
from ocpi.modules.versions.enums import VersionNumber
from tests.test_modules.test_v_2_3_0.test_bookings.utils import (
    ADAPTER,
    BOOKING_ID,
    BOOKINGS,
    ClientAuthenticator,
    Crud,
)
from tests.test_modules.utils import ENCODED_AUTH_TOKEN_V_2_3_0

EMSP_BASE_URL = "/ocpi/emsp/2.3.0"


@pytest.fixture
def client():
    """Create test client for EMSP bookings API."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[RoleEnum.emsp],
        modules=[ModuleID.bookings],
        authenticator=ClientAuthenticator,
        crud=Crud,
        adapter=ADAPTER,
    )
    return TestClient(app)


@pytest.fixture
def auth_headers():
    """Create authorization headers with Base64 encoded token (token_c)."""
    return {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}


class TestEMSPBookingsGet:
    """Tests for GET /bookings endpoints."""

    def test_get_bookings_list(self, client, auth_headers):
        """Test getting list of bookings."""
        response = client.get(f"{EMSP_BASE_URL}/bookings", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
        assert isinstance(data["data"], list)

    def test_get_booking_by_id(self, client, auth_headers):
        """Test getting a specific booking by country_code/party_id/booking_id."""
        response = client.get(
            f"{EMSP_BASE_URL}/bookings/DE/ELU/{BOOKING_ID}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
        # Check that we got a booking data object
        assert "id" in data["data"]


class TestEMSPBookingsPut:
    """Tests for PUT /bookings/{country_code}/{party_id}/{booking_id} endpoint."""

    def test_add_or_update_booking(self, client, auth_headers):
        """Test adding or updating a booking (push from CPO)."""
        booking_data = BOOKINGS[0].copy()
        booking_data["state"] = BookingState.active
        booking_data["last_updated"] = datetime.now(UTC).isoformat()

        response = client.put(
            f"{EMSP_BASE_URL}/bookings/DE/ELU/{BOOKING_ID}",
            json=booking_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000


class TestEMSPBookingsPatch:
    """Tests for PATCH /bookings/{country_code}/{party_id}/{booking_id} endpoint."""

    def test_partial_update_booking(self, client, auth_headers):
        """Test partially updating a booking."""
        update_data = {"state": BookingState.completed}

        response = client.patch(
            f"{EMSP_BASE_URL}/bookings/DE/ELU/{BOOKING_ID}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000


class TestEMSPBookingsDelete:
    """Tests for DELETE /bookings/{country_code}/{party_id}/{booking_id} endpoint."""

    def test_delete_booking(self, client, auth_headers):
        """Test deleting a booking."""
        response = client.delete(
            f"{EMSP_BASE_URL}/bookings/DE/ELU/{BOOKING_ID}",
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status_code"] == 1000
