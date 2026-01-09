# Charge Detail Records (CDRs)

This tutorial demonstrates how to create and manage Charge Detail Records (CDRs) in an OCPI application.

## Overview

CDRs are billing records that contain detailed information about a charging session, including:
- Energy consumed
- Cost breakdown
- Tariff information
- Time details
- Location information

## Setup

Include the CDRs module:

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo, RoleEnum.emsp],
    modules=[ModuleID.cdrs],
    authenticator=YourAuthenticator,
    crud=YourCrud,
)
```

## Creating a CDR

### Basic CDR

```python
cdr_data = {
    "country_code": "DK",
    "party_id": "ABC",
    "id": "CDR001",
    "start_date_time": "2024-01-01T10:00:00Z",
    "end_date_time": "2024-01-01T11:00:00Z",
    "session_id": "SESS001",
    "cdr_token": {
        "uid": "TOKEN123",
        "type": "RFID",
        "contract_id": "CONTRACT001"
    },
    "auth_method": "AUTH_REQUEST",
    "location": {
        "id": "LOC001",
        "name": "Copenhagen Central Charging Station",
        "address": "Strøget 1",
        "city": "Copenhagen",
        "postal_code": "1000",
        "country": "DNK",
        "coordinates": {
            "latitude": "55.6761",
            "longitude": "12.5683"
        },
        "evse": {
            "uid": "EVSE001",
            "evse_id": "EVSE001",
            "connector_id": "CONN001"
        }
    },
    "currency": "DKK",
    "tariffs": [],
    "charging_periods": [],
    "total_cost": 0.0,
    "total_energy": 30.0,
    "total_time": 3600,
    "last_updated": "2024-01-01T11:00:00Z"
}
```

### CDR with Tariff

```python
cdr_data = {
    # ... basic fields ...
    "tariffs": [
        {
            "country_code": "DK",
            "party_id": "ABC",
            "id": "TARIFF001",
            "currency": "DKK",
            "type": "REGULAR",
            "tariff_alt_text": [],
            "tariff_alt_url": "https://example.com/tariff",
            "min_price": {
                "excl_vat": 0.0,
                "incl_vat": 0.0
            },
            "max_price": {
                "excl_vat": 50.0,
                "incl_vat": 55.0
            },
            "elements": [
                {
                    "price_components": [
                        {
                            "type": "ENERGY",
                            "price": 0.25,
                            "step_size": 1
                        }
                    ]
                }
            ],
            "last_updated": "2024-01-01T00:00:00Z"
        }
    ],
    "total_cost": 7.50
}
```

### CDR with Charging Periods

```python
cdr_data = {
    # ... basic fields ...
    "charging_periods": [
        {
            "start_date_time": "2024-01-01T10:00:00Z",
            "dimensions": [
                {
                    "type": "ENERGY",
                    "volume": 30.0
                },
                {
                    "type": "TIME",
                    "volume": 3600.0
                }
            ],
            "tariff_id": "TARIFF001"
        }
    ]
}
```

## CRUD Operations

### Create CDR

```python
class YourCrud(Crud):
    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> dict:
        """Create a new CDR."""
        cdr_id = data.get("id")
        # Store in your database
        # Generate invoice if needed
        # ...
        return data
```

### Get CDR

```python
@classmethod
async def get(
    cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
) -> dict | None:
    """Get a CDR by ID."""
    # Retrieve from database
    # ...
    return cdr_data
```

### List CDRs

```python
@classmethod
async def list(
    cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
) -> tuple[list[dict], int, bool]:
    """Get paginated list of CDRs."""
    # Filter by date_from, date_to, etc.
    # ...
    return cdrs, total_count, is_last_page
```

## API Usage

### Create CDR (POST)

```bash
curl -X POST 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/cdrs' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d @cdr.json
```

### Get CDR (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/cdrs/DK/ABC/CDR001' \
  -H 'Authorization: Token your-token'
```

### List CDRs (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/cdrs/?date_from=2024-01-01T00:00:00Z' \
  -H 'Authorization: Token your-token'
```

## Cost Calculation

### Energy Cost

```python
energy_cost = total_energy * energy_price_per_kwh
```

### Time Cost

```python
time_cost = (total_time / 3600) * time_price_per_hour
```

### Total Cost

```python
total_cost = energy_cost + time_cost + parking_cost + fixed_cost
```

## Dimensions

CDR dimensions track different cost components:

- **ENERGY** - Energy consumed (kWh)
- **TIME** - Time duration (seconds)
- **PARKING_TIME** - Parking duration
- **MAX_CURRENT** - Maximum current
- **MIN_CURRENT** - Minimum current
- **MAX_POWER** - Maximum power
- **MIN_POWER** - Minimum power

## Best Practices

1. **Generate after session** - Create CDR after session completes
2. **Include all costs** - Calculate and include all cost components
3. **Link to session** - Always reference the session_id
4. **Tariff information** - Include tariff details for transparency
5. **Accurate timestamps** - Ensure start/end times are accurate
6. **Currency consistency** - Use consistent currency throughout

## Complete Example

See the [Full CPO Example](../../examples/full_cpo/) which includes CDR generation.
