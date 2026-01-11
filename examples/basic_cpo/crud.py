"""Simple CRUD implementation for the basic CPO example.

This uses in-memory storage. In production, replace with a real database.
"""

from typing import Any

from ocpi.core.crud import Crud
from ocpi.core.enums import ModuleID, RoleEnum

# Simple in-memory storage (use a database in production!)
storage: dict[str, dict] = {}

# Pre-populate with example location for demonstration
storage["locations:LOC001"] = {
    "country_code": "DE",
    "party_id": "ABC",
    "id": "LOC001",
    "publish": True,
    "name": "Berlin Central Charging Station",
    "address": "Unter den Linden 1",
    "city": "Berlin",
    "postal_code": "10117",
    "country": "DEU",
    "coordinates": {"latitude": "52.5200", "longitude": "13.4050"},
    "time_zone": "Europe/Berlin",  # Required field
    "last_updated": "2024-01-01T00:00:00Z",
    # Optional fields (state, parking_type, operator, etc.) will default to None
    # Optional lists (evses, facilities, etc.) will default to []
}

# Pre-populate with example session for demonstration
# Session schema matches OCPI 2.3.0 specification
storage["sessions:SESS001"] = {
    # Required fields
    "country_code": "DE",  # ISO-3166 alpha-2 country code of the CPO
    "party_id": "ABC",  # ID of the CPO (ISO15118 standard)
    "id": "SESS001",  # Unique id that identifies the charging session
    "start_date_time": "2024-01-01T10:00:00Z",  # Timestamp when session became ACTIVE
    "end_date_time": None,  # Optional: timestamp when session was completed
    "kwh": 15.5,  # How many kWh were charged
    "cdr_token": {  # Required: Token used to start this charging session
        "country_code": "DE",
        "party_id": "ABC",
        "uid": "RFID123456",  # Unique identification by eMSP
        "type": "RFID",  # TokenType enum value
        "contract_id": "CONTRACT001",  # Unique identification by CPO
    },
    "auth_method": "WHITELIST",  # Required: AuthMethod enum (WHITELIST, COMMAND, or AUTH_REQUEST)
    "location_id": "LOC001",  # Location.id of the Location object
    "evse_uid": "EVSE001",  # EVSE.uid of the EVSE
    "connector_id": "CONN001",  # Connector.id of the Connector
    "currency": "EUR",  # ISO 4217 code of the currency
    "status": "ACTIVE",  # SessionStatus enum (ACTIVE, COMPLETED, INVALID, PENDING, RESERVATION)
    "last_updated": "2024-01-01T10:30:00Z",  # Timestamp when this Session was last updated
    # Optional fields
    "authorization_reference": None,  # Reference to the authorization given by the eMSP
    "meter_id": "METER001",  # Optional identification of the kWh meter
    "charging_periods": [],  # Optional list of Charging Periods
    "total_cost": None,  # Optional: total cost of the session in the specified currency
}


class SimpleCrud(Crud):
    """Simple CRUD implementation using in-memory storage."""

    @classmethod
    async def get(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> dict | None:
        """Get a single object by ID."""
        key = f"{module.value}:{id}"
        return storage.get(key)

    @classmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> tuple[list[dict], int, bool]:
        """Get a paginated list of objects."""
        # Simple implementation - return all items
        # In production, implement proper pagination using filters
        items = [v for k, v in storage.items() if k.startswith(f"{module.value}:")]
        total = len(items)
        is_last_page = True
        return items, total, is_last_page

    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> dict:
        """Create a new object."""
        location_id = data.get("id")
        key = f"{module.value}:{location_id}"
        storage[key] = data
        return data

    @classmethod
    async def update(
        cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs
    ) -> dict:
        """Update an existing object."""
        key = f"{module.value}:{id}"
        if key in storage:
            storage[key].update(data)
            return storage[key]
        return data

    @classmethod
    async def delete(
        cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
    ) -> None:
        """Delete an object."""
        key = f"{module.value}:{id}"
        storage.pop(key, None)

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
        """Handle non-CRUD actions."""
        # Implement action-specific logic here
        return {}
