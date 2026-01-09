# Managing Locations

This tutorial demonstrates how to manage charging locations in an OCPI CPO application.

## Overview

Locations represent charging stations where electric vehicles can be charged. Each location contains:
- Basic information (name, address, coordinates)
- EVSEs (Electric Vehicle Supply Equipment)
- Connectors
- Tariffs
- Operating hours
- And more

## Setup

First, ensure your application includes the locations module:

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.locations],
    authenticator=YourAuthenticator,
    crud=YourCrud,
)
```

## Creating a Location

### Basic Location

```python
location_data = {
    "country_code": "DE",
    "party_id": "ABC",
    "id": "LOC001",
    "publish": True,
    "name": "Berlin Central Charging Station",
    "address": "Unter den Linden 1",
    "city": "Berlin",
    "postal_code": "10117",
    "country": "DEU",
    "coordinates": {
        "latitude": "52.5200",
        "longitude": "13.4050"
    },
    "evses": [],
    "last_updated": "2024-01-01T00:00:00Z"
}
```

### Location with EVSEs and Connectors

```python
location_data = {
    "country_code": "ES",
    "party_id": "ABC",
    "id": "LOC001",
    "publish": True,
    "name": "Madrid Premium Charging Hub",
    "address": "Gran Vía 1",
    "city": "Madrid",
    "postal_code": "28013",
    "country": "ESP",
    "coordinates": {
        "latitude": "40.4168",
        "longitude": "-3.7038"
    },
    "evses": [
        {
            "uid": "EVSE001",
            "evse_id": "EVSE001",
            "status": "AVAILABLE",
            "capabilities": ["CREDIT_CARD_PAYABLE"],
            "connectors": [
                {
                    "id": "CONN001",
                    "standard": "IEC_62196_T2",
                    "format": "SOCKET",
                    "power_type": "AC_3_PHASE",
                    "max_voltage": 400,
                    "max_amperage": 32,
                    "max_electric_power": 22000,
                    "tariff_ids": ["TARIFF001"],
                    "last_updated": "2024-01-01T00:00:00Z"
                }
            ],
            "last_updated": "2024-01-01T00:00:00Z"
        }
    ],
    "last_updated": "2024-01-01T00:00:00Z"
}
```

## CRUD Operations

### Create/Update Location

```python
class YourCrud(Crud):
    @classmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> dict:
        """Create a new location."""
        location_id = data.get("id")
        # Store in your database
        # ...
        return data
    
    @classmethod
    async def update(
        cls, module: ModuleID, role: RoleEnum, data: dict, id: str, *args, **kwargs
    ) -> dict:
        """Update an existing location."""
        # Update in your database
        # ...
        return updated_data
```

### Get Location

```python
@classmethod
async def get(
    cls, module: ModuleID, role: RoleEnum, id: str, *args, **kwargs
) -> dict | None:
    """Get a location by ID."""
    # Retrieve from your database
    # ...
    return location_data
```

### List Locations

```python
@classmethod
async def list(
    cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
) -> tuple[list[dict], int, bool]:
    """Get paginated list of locations."""
    # Implement pagination using filters
    offset = filters.get("offset", 0)
    limit = filters.get("limit", 100)
    date_from = filters.get("date_from")
    date_to = filters.get("date_to")
    
    # Query your database
    # ...
    
    return locations, total_count, is_last_page
```

## API Usage

### Create/Update Location (PUT)

```bash
curl -X PUT 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/DE/ABC/LOC001' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d @location.json
```

### Get Location (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/DE/ABC/LOC001' \
  -H 'Authorization: Token your-token'
```

### List Locations (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/?offset=0&limit=100' \
  -H 'Authorization: Token your-token'
```

### Partial Update (PATCH)

```bash
curl -X PATCH 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/DE/ABC/LOC001' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "name": "Updated Location Name"
  }'
```

## Advanced Features

### Operating Hours

```python
location_data["opening_times"] = {
    "twentyfourseven": False,
    "regular_hours": [
        {
            "weekday": 1,  # Monday
            "period_begin": "08:00",
            "period_end": "22:00"
        },
        # ... other weekdays
    ],
    "exceptional_openings": [],
    "exceptional_closings": []
}
```

### Energy Mix

```python
location_data["energy_mix"] = {
    "is_green_energy": True,
    "energy_sources": [
        {"source": "SOLAR", "percentage": 60},
        {"source": "WIND", "percentage": 40}
    ],
    "supplier_name": "Green Energy Co",
    "energy_product_name": "100% Renewable"
}
```

### Images

```python
location_data["images"] = [
    {
        "url": "https://example.com/location.jpg",
        "thumbnail": "https://example.com/location-thumb.jpg",
        "category": "NETWORK",
        "type": "jpeg",
        "width": 1920,
        "height": 1080
    }
]
```

## Best Practices

1. **Always set `last_updated`** - This timestamp is crucial for synchronization
2. **Use proper coordinates** - Ensure latitude/longitude are valid
3. **Publish status** - Set `publish: true` for locations visible to EMSPs
4. **EVSE status** - Keep EVSE status updated (AVAILABLE, CHARGING, etc.)
5. **Tariff references** - Link connectors to tariffs using `tariff_ids`

## Complete Example

See the [Basic CPO Example](../../examples/basic_cpo/) for a complete working implementation.
