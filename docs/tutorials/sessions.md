# Managing Sessions

This tutorial demonstrates how to manage charging sessions in an OCPI application.

## Overview

Sessions represent active charging events. They track:
- When charging started/stopped
- Energy consumed (kWh)
- Cost information
- Location and connector details
- Status (ACTIVE, COMPLETED, etc.)

## Setup

Include the sessions module in your application:

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo, RoleEnum.emsp],
    modules=[ModuleID.sessions],
    authenticator=YourAuthenticator,
    crud=YourCrud,
)
```

## Session Lifecycle

### 1. Start Session (EMSP)

An EMSP starts a session when a user begins charging:

```python
session_data = {
    "country_code": "ES",
    "party_id": "ABC",
    "id": "SESS001",
    "start_date_time": "2024-01-01T10:00:00Z",
    "location_id": "LOC001",
    "evse_uid": "EVSE001",
    "connector_id": "CONN001",
    "kwh": 0.0,
    "currency": "EUR",
    "status": "ACTIVE",
    "last_updated": "2024-01-01T10:00:00Z"
}
```

### 2. Update Session (CPO)

The CPO updates the session as charging progresses:

```python
# Update energy consumed
updated_session = {
    "kwh": 15.5,
    "status": "ACTIVE",
    "last_updated": "2024-01-01T10:30:00Z"
}
```

### 3. End Session (CPO)

When charging completes:

```python
ended_session = {
    "end_date_time": "2024-01-01T11:00:00Z",
    "kwh": 30.0,
    "status": "COMPLETED",
    "last_updated": "2024-01-01T11:00:00Z"
}
```

## CRUD Operations

### Create Session

```python
class YourCrud(Crud):
    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> dict:
        """Create a new session."""
        session_id = data.get("id")
        # Store in your database
        # ...
        return data
```

### Update Session

```python
@classmethod
async def update(
    cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs
) -> dict:
    """Update an existing session."""
    # Update energy, status, etc.
    # ...
    return updated_data
```

### Get Session

```python
@classmethod
async def get(
    cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
) -> dict | None:
    """Get a session by ID."""
    # Retrieve from database
    # ...
    return session_data
```

### List Sessions

```python
@classmethod
async def list(
    cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
) -> tuple[list[dict], int, bool]:
    """Get paginated list of sessions."""
    # Filter by date_from, date_to, etc.
    # ...
    return sessions, total_count, is_last_page
```

## Session Status

Common session statuses:

- **ACTIVE** - Charging is in progress
- **COMPLETED** - Charging finished normally
- **INVALID** - Session data is invalid
- **PENDING** - Session is pending start

## API Usage

### Create/Update Session (PUT)

```bash
curl -X PUT 'http://127.0.0.1:8000/ocpi/emsp/2.3.0/sessions/ES/ABC/SESS001' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d @session.json
```

### Get Session (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/sessions/ES/ABC/SESS001' \
  -H 'Authorization: Token your-token'
```

### List Sessions (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/sessions/?date_from=2024-01-01T00:00:00Z' \
  -H 'Authorization: Token your-token'
```

### Partial Update (PATCH)

```bash
curl -X PATCH 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/sessions/ES/ABC/SESS001' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "kwh": 25.5,
    "status": "ACTIVE"
  }'
```

## Advanced Features

### Charging Preferences (OCPI 2.2.1+)

```python
session_data["charging_preferences"] = {
    "profile_type": "FAST",
    "departure_time": "2024-01-01T12:00:00Z",
    "energy_need": 50.0
}
```

### Meter Values

```python
session_data["meter_value"] = [
    {
        "timestamp": "2024-01-01T10:00:00Z",
        "sampled_value": [
            {
                "value": "0.0",
                "context": "Sample.Periodic",
                "measurand": "Energy.Active.Import.Register",
                "unit": "kWh"
            }
        ]
    }
]
```

## Best Practices

1. **Update frequently** - Update session energy consumption regularly
2. **Set timestamps** - Always include `start_date_time` and `end_date_time`
3. **Track status** - Keep session status accurate
4. **Link to location** - Always reference the correct location and EVSE
5. **Calculate costs** - Include cost information when available

## Complete Example

See the [EMSP Sessions Example](../../examples/emsp_sessions/) for a complete working implementation.
