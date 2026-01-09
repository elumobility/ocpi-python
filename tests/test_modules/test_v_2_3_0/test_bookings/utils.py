"""Test utilities for OCPI 2.3.0 Bookings module."""

import copy
from datetime import UTC, datetime, timedelta

from ocpi.core.adapter import BaseAdapter
from ocpi.core.crud import Crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.bookings.v_2_3_0.enums import BookingState
from ocpi.modules.tokens.v_2_3_0.enums import TokenType, WhitelistType
from tests.test_modules.utils import ClientAuthenticator

__all__ = ["ClientAuthenticator", "ADAPTER", "BOOKING_ID", "BOOKINGS", "Crud"]

# Sample booking data
BOOKING_ID = "BOOKING-001"
LOCATION_ID = "LOC-001"
EVSE_UID = "EVSE-001"
CONNECTOR_ID = "CONN-001"
EMSP_BOOKING_ID = "EMSP-BOOKING-001"


def get_token_data():
    """Return fresh token data for each test."""
    return {
        "country_code": "DE",
        "party_id": "ELU",
        "uid": "TOKEN-001",
        "type": TokenType.rfid,
        "contract_id": "CONTRACT-001",
        "visual_number": "12345678",
        "issuer": "ELU Mobility",
        "group_id": None,
        "valid": True,
        "whitelist": WhitelistType.always,
        "language": "de",
        "default_profile_type": None,
        "energy_contract": None,
        "last_updated": datetime.now(UTC).isoformat(),
    }


def get_bookings():
    """Return fresh booking data for each test - avoids test isolation issues."""
    return [
        {
            "country_code": "DE",
            "party_id": "ELU",
            "id": BOOKING_ID,
            "emsp_booking_id": EMSP_BOOKING_ID,
            "token": get_token_data(),
            "location_id": LOCATION_ID,
            "evse_uid": EVSE_UID,
            "connector_id": CONNECTOR_ID,
            "start_date_time": (datetime.now(UTC) + timedelta(hours=1)).isoformat(),
            "end_date_time": (datetime.now(UTC) + timedelta(hours=3)).isoformat(),
            "state": BookingState.confirmed,
            "authorization_reference": "AUTH-REF-001",
            "energy_estimate": 50.0,
            "estimated_cost": {"excl_vat": 25.00, "incl_vat": 29.75},
            "status_message": [],
            "session_id": None,
            "last_updated": datetime.now(UTC).isoformat(),
        }
    ]


# Keep for backward compatibility but use fresh copy
TOKEN_DATA = get_token_data()
BOOKINGS = get_bookings()


class Crud(Crud):
    # Class-level storage that resets for each test class
    _bookings = None

    @classmethod
    def _get_bookings(cls):
        """Get bookings, initializing fresh data if needed."""
        if cls._bookings is None:
            cls._bookings = get_bookings()
        return cls._bookings

    @classmethod
    def _reset_bookings(cls):
        """Reset bookings to fresh state."""
        cls._bookings = get_bookings()

    @classmethod
    async def list(
        cls,
        module: ModuleID,
        role: RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> tuple[list, int, bool]:
        bookings = cls._get_bookings()
        return bookings, len(bookings), True

    @classmethod
    async def get(
        cls,
        module: ModuleID,
        role: RoleEnum,
        id: str,
        *args,
        **kwargs,
    ):
        bookings = cls._get_bookings()
        for booking in bookings:
            if booking["id"] == id:
                return copy.deepcopy(booking)
        return None

    @classmethod
    async def create(
        cls,
        module: ModuleID,
        role: RoleEnum,
        data: dict,
        *args,
        **kwargs,
    ):
        bookings = cls._get_bookings()
        # Create a new booking from request data
        new_booking = {
            "country_code": "DE",
            "party_id": "ELU",
            "id": f"BOOKING-{len(bookings) + 1:03d}",
            "emsp_booking_id": data.get("emsp_booking_id"),
            "token": data.get("token"),
            "location_id": data.get("location_id"),
            "evse_uid": data.get("evse_uid"),
            "connector_id": data.get("connector_id"),
            "start_date_time": data.get("start_date_time"),
            "end_date_time": data.get("end_date_time"),
            "state": BookingState.confirmed,
            "authorization_reference": data.get("authorization_reference"),
            "energy_estimate": data.get("energy_estimate"),
            "estimated_cost": None,
            "status_message": [],
            "session_id": None,
            "last_updated": datetime.now(UTC).isoformat(),
        }
        return new_booking

    @classmethod
    async def update(
        cls,
        module: ModuleID,
        role: RoleEnum,
        data: dict,
        id: str,
        *args,
        **kwargs,
    ):
        bookings = cls._get_bookings()
        country_code = kwargs.get("country_code")
        party_id = kwargs.get("party_id")

        for booking in bookings:
            if booking["id"] == id:
                # If country_code and party_id are provided, verify they match
                if country_code and party_id:
                    if (
                        booking["country_code"] == country_code
                        and booking["party_id"] == party_id
                    ):
                        # Return updated copy without mutating original
                        updated = copy.deepcopy(booking)
                        updated.update(data)
                        updated["last_updated"] = datetime.now(UTC).isoformat()
                        return updated
                else:
                    # Return updated copy without mutating original
                    updated = copy.deepcopy(booking)
                    updated.update(data)
                    updated["last_updated"] = datetime.now(UTC).isoformat()
                    return updated
        return None

    @classmethod
    async def delete(
        cls,
        module: ModuleID,
        role: RoleEnum,
        id: str,
        *args,
        **kwargs,
    ):
        return None


ADAPTER = BaseAdapter
