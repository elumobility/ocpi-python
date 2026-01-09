"""CRUD implementation for the bookings example.

This uses in-memory storage. In production, replace with a real database.
"""

import uuid
from datetime import UTC, datetime
from typing import Any

from ocpi.core.crud import Crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.bookings.v_2_3_0.enums import BookingState

# Simple in-memory storage (use a database in production!)
bookings_storage: dict[str, dict] = {}


class BookingsCrud(Crud):
    """CRUD implementation for bookings with in-memory storage."""

    @classmethod
    async def get(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> dict | None:
        """Get a booking by ID."""
        # Use lowercase for lookup (CiString lowercases values)
        return bookings_storage.get(id.lower())

    @classmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> tuple[list[dict], int, bool]:
        """Get a paginated list of bookings."""
        # Apply date filters if provided
        items = list(bookings_storage.values())

        date_from = filters.get("date_from")
        date_to = filters.get("date_to")

        if date_from:
            items = [b for b in items if b.get("last_updated", "") >= date_from]
        if date_to:
            items = [b for b in items if b.get("last_updated", "") <= date_to]

        # Apply pagination
        offset = filters.get("offset", 0)
        limit = filters.get("limit", 50)
        paginated = items[offset : offset + limit]

        total = len(items)
        is_last_page = offset + limit >= total

        return paginated, total, is_last_page

    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> dict:
        """Create a new booking from a booking request."""
        # Generate booking ID if not provided
        # Use lowercase to match CiString behavior (case-insensitive strings are lowercased)
        booking_id = data.get("id") or f"booking-{uuid.uuid4().hex[:8].lower()}"

        # Create booking from request
        booking = {
            "country_code": kwargs.get("country_code", "DE"),
            "party_id": kwargs.get("party_id", "ELU"),
            "id": booking_id,
            "emsp_booking_id": data.get("emsp_booking_id"),
            "token": data.get("token"),
            "location_id": data.get("location_id"),
            "evse_uid": data.get("evse_uid"),
            "connector_id": data.get("connector_id"),
            "start_date_time": data.get("start_date_time"),
            "end_date_time": data.get("end_date_time"),
            "state": BookingState.confirmed,  # Auto-confirm for demo
            "authorization_reference": data.get("authorization_reference"),
            "energy_estimate": data.get("energy_estimate"),
            "estimated_cost": None,  # Calculate based on tariff in production
            "status_message": [],
            "session_id": None,
            "last_updated": datetime.now(UTC).isoformat(),
        }

        bookings_storage[booking_id] = booking
        return booking

    @classmethod
    async def update(
        cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs
    ) -> dict | None:
        """Update an existing booking."""
        # Use lowercase for lookup (CiString lowercases values)
        id_lower = id.lower()
        if id_lower not in bookings_storage:
            return None

        booking = bookings_storage[id_lower]

        # Update fields from data
        for key, value in data.items():
            if value is not None:
                booking[key] = value

        booking["last_updated"] = datetime.now(UTC).isoformat()
        return booking

    @classmethod
    async def delete(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> None:
        """Cancel/delete a booking."""
        # Use lowercase for lookup (CiString lowercases values)
        id_lower = id.lower()
        if id_lower in bookings_storage:
            # Mark as cancelled rather than deleting
            bookings_storage[id_lower]["state"] = BookingState.cancelled
            bookings_storage[id_lower]["last_updated"] = datetime.now(UTC).isoformat()

    @classmethod
    async def do(
        cls,
        module: ModuleID,
        role: RoleEnum | None,
        action: Any,
        *args,
        data: dict | None = None,
        **kwargs,
    ) -> Any:
        """Handle non-CRUD actions for bookings."""
        # Could implement actions like:
        # - Check availability for a time slot
        # - Extend booking duration
        # - Convert booking to session
        return {}
