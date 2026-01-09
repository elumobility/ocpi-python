# Charging Profiles

This tutorial demonstrates how to manage charging profiles for smart charging (OCPI 2.2.1+).

## Overview

Charging profiles allow control of charging power over time, enabling:
- Load balancing
- Grid optimization
- Cost optimization
- Renewable energy integration

## Setup

Include the charging profiles module:

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.charging_profile, ModuleID.sessions],
    authenticator=YourAuthenticator,
    crud=YourCrud,
)
```

## Setting a Charging Profile

### Basic Charging Profile

```python
charging_profile_data = {
    "charging_profile": {
        "start_date_time": "2024-01-01T10:00:00Z",
        "charging_rate_unit": "A",
        "charging_schedule": {
            "start_schedule": "2024-01-01T10:00:00Z",
            "charging_rate_unit": "A",
            "charging_periods": [
                {
                    "start_period": 0,
                    "limit": 16.0
                }
            ]
        }
    },
    "response_url": "https://emsp.example.com/chargingprofiles/response"
}
```

### Advanced Charging Profile

```python
charging_profile_data = {
    "charging_profile": {
        "start_date_time": "2024-01-01T10:00:00Z",
        "duration": 7200,  # 2 hours
        "charging_rate_unit": "A",
        "charging_schedule": {
            "start_schedule": "2024-01-01T10:00:00Z",
            "charging_rate_unit": "A",
            "charging_periods": [
                {
                    "start_period": 0,
                    "limit": 16.0,
                    "number_phases": 3
                },
                {
                    "start_period": 1800,  # After 30 minutes
                    "limit": 32.0,
                    "number_phases": 3
                }
            ]
        }
    },
    "response_url": "https://emsp.example.com/chargingprofiles/response"
}
```

## Charging Rate Units

- **A** - Amperes (current)
- **W** - Watts (power)

## Implementing Charging Profile Handling

```python
from ocpi.core.enums import Action, ModuleID, RoleEnum

class YourCrud(Crud):
    @classmethod
    async def do(
        cls,
        module: ModuleID,
        role: RoleEnum | None,
        action: Action,
        *args,
        data: dict | None = None,
        **kwargs,
    ) -> dict:
        """Handle charging profile actions."""
        if module == ModuleID.charging_profile:
            session_id = kwargs.get("session_id")
            duration = kwargs.get("duration")
            
            if action == Action.send_update_charging_profile:
                # Set or update charging profile
                charging_profile = data.get("charging_profile") if data else None
                
                if charging_profile and session_id:
                    # Store charging profile
                    # Send to charge point via OCPP SetChargingProfile
                    result = await send_ocpp_set_charging_profile(
                        session_id, charging_profile
                    )
                    
                    return {
                        "result": "ACCEPTED" if result else "REJECTED"
                    }
            
            elif action == Action.send_get_chargingprofile:
                # Get active charging profile
                profile = await get_active_charging_profile(session_id, duration)
                
                return {
                    "result": "ACCEPTED",
                    "charging_profile": profile
                }
            
            elif action == Action.send_delete_chargingprofile:
                # Clear charging profile
                result = await clear_charging_profile(session_id)
                
                return {
                    "result": "ACCEPTED" if result else "REJECTED"
                }
        
        return {}
```

## Charging Profile Results

Possible results:

- **ACCEPTED** - Profile was accepted
- **NOT_SUPPORTED** - Not supported by charge point
- **REJECTED** - Profile was rejected
- **UNKNOWN_SESSION** - Session not found

## API Usage

### Set Charging Profile (PUT)

```bash
curl -X PUT 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/chargingprofiles/SESS001' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d @charging_profile.json
```

### Get Active Charging Profile (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/chargingprofiles/SESS001?duration=3600' \
  -H 'Authorization: Token your-token'
```

### Clear Charging Profile (DELETE)

```bash
curl -X DELETE 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/chargingprofiles/SESS001' \
  -H 'Authorization: Token your-token'
```

## Charging Periods

Charging periods define power limits over time:

```python
charging_periods = [
    {
        "start_period": 0,  # Start immediately
        "limit": 16.0,  # 16A limit
        "number_phases": 3  # 3-phase charging
    },
    {
        "start_period": 1800,  # After 30 minutes (1800 seconds)
        "limit": 32.0,  # Increase to 32A
        "number_phases": 3
    }
]
```

## Best Practices

1. **Validate profiles** - Check profile validity before applying
2. **Handle timeouts** - Set appropriate timeouts for profile operations
3. **Monitor sessions** - Ensure session is active before setting profiles
4. **Send responses** - Always send results to response_url
5. **Error handling** - Handle OCPP communication errors
6. **Profile persistence** - Store profiles for session duration

## Complete Example

See the [Charging Profiles Example](../../examples/charging_profiles/) for a complete working implementation.
