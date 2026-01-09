# Booking Reservations

This tutorial covers implementing EV charging reservations using the OCPI 2.3.0 Booking module.

!!! note "OCPI 2.3.0 Feature"
    The Booking module is new in OCPI 2.3.0. It allows EMSPs to reserve charging time slots at CPO charging stations.

## Overview

The Booking module enables:

- **Time slot reservations** - Reserve specific charging times in advance
- **Booking lifecycle management** - Track bookings from request to completion
- **Integration with sessions** - Convert confirmed bookings to charging sessions

## Booking States

```mermaid
stateDiagram-v2
    [*] --> PENDING: Request received
    PENDING --> CONFIRMED: CPO accepts
    PENDING --> REJECTED: CPO rejects
    CONFIRMED --> ACTIVE: Session starts
    CONFIRMED --> CANCELLED: User cancels
    CONFIRMED --> EXPIRED: Time passes
    ACTIVE --> COMPLETED: Session ends
    COMPLETED --> [*]
    REJECTED --> [*]
    CANCELLED --> [*]
    EXPIRED --> [*]
```

| State | Description |
|-------|-------------|
| `PENDING` | Booking request received, awaiting CPO confirmation |
| `CONFIRMED` | CPO has confirmed the booking |
| `ACTIVE` | Charging session is in progress |
| `COMPLETED` | Booking completed successfully |
| `CANCELLED` | Booking was cancelled |
| `EXPIRED` | Booking expired without being used |
| `REJECTED` | CPO rejected the booking request |
| `FAILED` | Booking could not be fulfilled |

## Setting Up a Booking Application

### Basic CPO Setup

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.bookings],
    authenticator=MyAuthenticator,
    crud=MyBookingsCrud,
)
```

### Implementing the CRUD

```python
from datetime import UTC, datetime
from ocpi.core.crud import Crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.bookings.v_2_3_0.enums import BookingState

class BookingsCrud(Crud):
    @classmethod
    async def get(cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs):
        """Retrieve a booking by ID."""
        # Query your database for the booking
        return await database.get_booking(id)
    
    @classmethod
    async def list(cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs):
        """List bookings with pagination."""
        # Apply filters (date_from, date_to, offset, limit)
        bookings = await database.list_bookings(
            date_from=filters.get("date_from"),
            date_to=filters.get("date_to"),
            offset=filters.get("offset", 0),
            limit=filters.get("limit", 50),
        )
        total = await database.count_bookings()
        is_last = filters.get("offset", 0) + len(bookings) >= total
        return bookings, total, is_last
    
    @classmethod
    async def create(cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs):
        """Process a booking request from an EMSP."""
        # Validate availability
        is_available = await check_availability(
            location_id=data["location_id"],
            evse_uid=data.get("evse_uid"),
            start_time=data["start_date_time"],
            end_time=data["end_date_time"],
        )
        
        if not is_available:
            return None  # Will result in REJECTED response
        
        # Create the booking
        booking = {
            "country_code": "DE",
            "party_id": "ELU",
            "id": generate_booking_id(),
            "emsp_booking_id": data["emsp_booking_id"],
            "token": data["token"],
            "location_id": data["location_id"],
            "evse_uid": data.get("evse_uid"),
            "connector_id": data.get("connector_id"),
            "start_date_time": data["start_date_time"],
            "end_date_time": data["end_date_time"],
            "state": BookingState.confirmed,
            "authorization_reference": data.get("authorization_reference"),
            "energy_estimate": data.get("energy_estimate"),
            "estimated_cost": calculate_estimated_cost(data),
            "status_message": [],
            "session_id": None,
            "last_updated": datetime.now(UTC).isoformat(),
        }
        
        await database.save_booking(booking)
        return booking
    
    @classmethod
    async def update(cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs):
        """Update a booking (e.g., change state)."""
        booking = await database.get_booking(id)
        if not booking:
            return None
        
        # Update allowed fields
        for key, value in data.items():
            if value is not None:
                booking[key] = value
        
        booking["last_updated"] = datetime.now(UTC).isoformat()
        await database.save_booking(booking)
        return booking
    
    @classmethod
    async def delete(cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs):
        """Cancel a booking."""
        booking = await database.get_booking(id)
        if booking:
            booking["state"] = BookingState.cancelled
            booking["last_updated"] = datetime.now(UTC).isoformat()
            await database.save_booking(booking)
```

## API Endpoints

### CPO Endpoints (Receiver)

The CPO receives booking requests from EMSPs:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ocpi/cpo/2.3.0/bookings` | List all bookings |
| GET | `/ocpi/cpo/2.3.0/bookings/{id}` | Get specific booking |
| POST | `/ocpi/cpo/2.3.0/bookings` | Create new booking |
| PATCH | `/ocpi/cpo/2.3.0/bookings/{id}` | Update booking |
| DELETE | `/ocpi/cpo/2.3.0/bookings/{id}` | Cancel booking |

### EMSP Endpoints (Sender)

The EMSP can query and manage bookings:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ocpi/emsp/2.3.0/bookings/{country_code}/{party_id}` | List bookings |
| GET | `/ocpi/emsp/2.3.0/bookings/{country_code}/{party_id}/{id}` | Get booking |
| PUT | `/ocpi/emsp/2.3.0/bookings/{country_code}/{party_id}/{id}` | Add/update booking |
| PATCH | `/ocpi/emsp/2.3.0/bookings/{country_code}/{party_id}/{id}` | Partial update |
| DELETE | `/ocpi/emsp/2.3.0/bookings/{country_code}/{party_id}/{id}` | Delete booking |

## Example: Creating a Booking Request

An EMSP sends a booking request to a CPO:

```python
import httpx
import base64

# Prepare the token (Base64 encoded for OCPI 2.3.0)
token = base64.b64encode(b"my-emsp-token").decode()

# Booking request
booking_request = {
    "emsp_booking_id": "EMSP-REQ-001",
    "token": {
        "country_code": "DE",
        "party_id": "EMS",
        "uid": "RFID-12345678",
        "type": "RFID",
        "contract_id": "DE-EMS-C12345678-1",
        "valid": True,
        "whitelist": "ALWAYS",
        "last_updated": "2026-01-09T12:00:00Z",
    },
    "location_id": "LOC-BERLIN-001",
    "evse_uid": "EVSE-001",
    "connector_id": "CONN-001",
    "start_date_time": "2026-01-10T14:00:00Z",
    "end_date_time": "2026-01-10T16:00:00Z",
    "energy_estimate": 30.0,
}

# Send request
async with httpx.AsyncClient() as client:
    response = await client.post(
        "https://cpo.example.com/ocpi/cpo/2.3.0/bookings",
        json=booking_request,
        headers={"Authorization": f"Token {token}"},
    )
    
    result = response.json()
    if result["data"]["result"] == "ACCEPTED":
        booking = result["data"]["booking"]
        print(f"Booking confirmed: {booking['id']}")
    else:
        print(f"Booking rejected: {result['data']['message']}")
```

## Example: Updating Booking State

When a charging session starts, update the booking to ACTIVE:

```python
async def start_session_from_booking(booking_id: str, session_id: str):
    """Convert a booking to an active session."""
    await crud.update(
        ModuleID.bookings,
        RoleEnum.cpo,
        {
            "state": BookingState.active,
            "session_id": session_id,
        },
        booking_id,
    )
```

## Booking → Session Integration

A key feature of the Booking module is linking reservations to actual charging sessions. This section demonstrates the complete workflow.

### Architecture Overview

```mermaid
sequenceDiagram
    participant EMSP
    participant CPO
    participant EVSE
    
    EMSP->>CPO: POST /bookings (BookingRequest)
    CPO-->>EMSP: BookingResponse (CONFIRMED)
    
    Note over EMSP,EVSE: User arrives at charging station
    
    EMSP->>CPO: POST /commands/START_SESSION
    CPO->>EVSE: Start charging
    EVSE-->>CPO: Session started
    CPO->>CPO: Create Session, link to Booking
    CPO-->>EMSP: PATCH /bookings (state=ACTIVE, session_id)
    CPO-->>EMSP: PUT /sessions (new session)
    
    Note over EMSP,EVSE: Charging completes
    
    EVSE-->>CPO: Session ended
    CPO->>CPO: Update Booking state=COMPLETED
    CPO-->>EMSP: PATCH /bookings (state=COMPLETED)
    CPO-->>EMSP: PATCH /sessions (status=COMPLETED)
```

### Complete Integration Example

Here's a full implementation showing how to convert a booking into a session:

```python
from datetime import UTC, datetime
import uuid

from ocpi.core.crud import Crud
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.bookings.v_2_3_0.enums import BookingState
from ocpi.modules.sessions.v_2_3_0.enums import SessionStatus


class IntegratedCrud(Crud):
    """CRUD that handles booking-to-session conversion."""
    
    @classmethod
    async def convert_booking_to_session(
        cls,
        booking_id: str,
        auth_method: str = "WHITELIST",
    ) -> dict:
        """
        Convert a confirmed booking into an active charging session.
        
        This is typically called when:
        1. User arrives and authenticates at the EVSE
        2. CPO receives START_SESSION command for a booked slot
        
        Args:
            booking_id: The booking to convert
            auth_method: How the user authenticated (WHITELIST, APP, etc.)
            
        Returns:
            The created session object
        """
        # 1. Retrieve the booking
        booking = await cls.get(ModuleID.bookings, RoleEnum.cpo, booking_id)
        if not booking:
            raise ValueError(f"Booking {booking_id} not found")
        
        if booking["state"] != BookingState.confirmed:
            raise ValueError(f"Booking must be CONFIRMED, got {booking['state']}")
        
        # 2. Create a new session linked to this booking
        session_id = f"SESSION-{uuid.uuid4().hex[:8].upper()}"
        now = datetime.now(UTC).isoformat()
        
        session = {
            "country_code": booking["country_code"],
            "party_id": booking["party_id"],
            "id": session_id,
            "start_date_time": now,
            "end_date_time": None,  # Session is ongoing
            "kwh": 0.0,
            "cdr_token": {
                "country_code": booking["token"]["country_code"],
                "party_id": booking["token"]["party_id"],
                "uid": booking["token"]["uid"],
                "type": booking["token"]["type"],
                "contract_id": booking["token"]["contract_id"],
            },
            "auth_method": auth_method,
            # Link session to booking via authorization_reference
            "authorization_reference": booking.get("authorization_reference"),
            "location_id": booking["location_id"],
            "evse_uid": booking["evse_uid"],
            "connector_id": booking["connector_id"],
            "meter_id": None,
            "currency": "EUR",
            "charging_periods": [],
            "total_cost": None,
            "status": SessionStatus.active,
            # New in OCPI 2.3.0 - EV battery info
            "soc_start": None,  # Can be populated from EVSE data
            "soc_end": None,
            "odometer": None,
            "last_updated": now,
        }
        
        # 3. Save the session
        await cls.create(ModuleID.sessions, RoleEnum.cpo, session)
        
        # 4. Update the booking with session_id and state
        await cls.update(
            ModuleID.bookings,
            RoleEnum.cpo,
            {
                "state": BookingState.active,
                "session_id": session_id,
                "last_updated": now,
            },
            booking_id,
        )
        
        return session
    
    @classmethod
    async def complete_booking_session(
        cls,
        booking_id: str,
        final_kwh: float,
        total_cost: dict | None = None,
    ) -> tuple[dict, dict]:
        """
        Complete a booking and its associated session.
        
        Args:
            booking_id: The booking to complete
            final_kwh: Total energy delivered (kWh)
            total_cost: Final cost (optional)
            
        Returns:
            Tuple of (updated_booking, updated_session)
        """
        booking = await cls.get(ModuleID.bookings, RoleEnum.cpo, booking_id)
        if not booking or not booking.get("session_id"):
            raise ValueError("Booking not found or has no linked session")
        
        now = datetime.now(UTC).isoformat()
        
        # 1. Update the session
        session = await cls.update(
            ModuleID.sessions,
            RoleEnum.cpo,
            {
                "end_date_time": now,
                "kwh": final_kwh,
                "total_cost": total_cost,
                "status": SessionStatus.completed,
                "last_updated": now,
            },
            booking["session_id"],
        )
        
        # 2. Update the booking
        booking = await cls.update(
            ModuleID.bookings,
            RoleEnum.cpo,
            {
                "state": BookingState.completed,
                "last_updated": now,
            },
            booking_id,
        )
        
        return booking, session
```

### Using Authorization Reference for Correlation

The `authorization_reference` field is key for linking bookings and sessions:

```python
# When creating a booking, EMSP provides authorization_reference
booking_request = {
    "emsp_booking_id": "EMSP-REQ-001",
    "authorization_reference": "AUTH-2026-001",  # EMSP's reference
    # ... other fields
}

# When session is created, CPO copies authorization_reference
session = {
    "authorization_reference": booking["authorization_reference"],
    # ... other fields
}

# EMSP can correlate booking and session using this reference
async def find_session_for_booking(authorization_reference: str):
    """Find the session created from a booking."""
    sessions = await database.find_sessions(
        authorization_reference=authorization_reference
    )
    return sessions[0] if sessions else None
```

### Pushing Updates to EMSP

When the booking state changes, notify the EMSP:

```python
import httpx

async def notify_emsp_booking_update(booking: dict, emsp_url: str, token: str):
    """Push booking update to EMSP."""
    async with httpx.AsyncClient() as client:
        await client.patch(
            f"{emsp_url}/ocpi/emsp/2.3.0/bookings/"
            f"{booking['country_code']}/{booking['party_id']}/{booking['id']}",
            json={
                "state": booking["state"],
                "session_id": booking.get("session_id"),
                "last_updated": booking["last_updated"],
            },
            headers={"Authorization": f"Token {token}"},
        )
```

## Complete Working Example

See the [Bookings Example](../../examples/bookings/) for a complete, runnable application demonstrating:

- CPO booking receiver endpoints
- In-memory storage (easily replaceable with a database)
- Authentication handling for OCPI 2.3.0
- Full booking lifecycle management

## Best Practices

1. **Validate availability** - Always check EVSE availability before confirming bookings
2. **Handle conflicts** - Implement proper locking for concurrent booking requests
3. **Set timeouts** - Auto-expire bookings that aren't used within a grace period
4. **Link to sessions** - Store the `session_id` when a booking converts to a session
5. **Send notifications** - Notify EMSPs when booking states change

## Next Steps

- Review the [Sessions Tutorial](sessions.md) for integrating bookings with sessions
- Explore the [Commands Tutorial](commands.md) for START_SESSION commands
- Check the [API Reference](../api/v_2_3_0.md) for complete endpoint documentation
