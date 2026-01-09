# Token Authorization

This tutorial demonstrates how to handle token authorization in an OCPI application.

## Overview

Tokens represent RFID cards, mobile apps, or other identifiers that authorize charging. The authorization process:
1. EMSP requests authorization for a token
2. CPO validates the token
3. CPO returns authorization status and location information

## Setup

Include the tokens module:

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo, RoleEnum.emsp],
    modules=[ModuleID.tokens],
    authenticator=YourAuthenticator,
    crud=YourCrud,
)
```

## Token Management

### Create/Update Token

```python
token_data = {
    "country_code": "CH",
    "party_id": "ABC",
    "uid": "TOKEN123",
    "type": "RFID",
    "auth_method": "AUTH_REQUEST",
    "issuer": "ChargePoint Inc",
    "valid": True,
    "whitelist": "ALWAYS",
    "language": "en",
    "last_updated": "2024-01-01T00:00:00Z"
}
```

## Token Authorization

### Implement Authorization Logic

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
        """Handle token authorization."""
        if module == ModuleID.tokens and action == Action.authorize_token:
            token_uid = kwargs.get("token_uid")
            location_id = data.get("location_id") if data else None
            evse_uids = data.get("evse_uids") if data else []
            
            # Check if token is valid
            token = await cls.get(ModuleID.tokens, role, token_uid)
            if not token or not token.get("valid"):
                return {
                    "status": "INVALID",
                    "location": None
                }
            
            # Check if token is whitelisted for this location
            # ... your authorization logic ...
            
            # Return authorization info
            return {
                "status": "ACCEPTED",
                "location": {
                    "location_id": location_id,
                    "evse_uids": evse_uids,
                    "connector_ids": ["CONN001"]
                }
            }
        
        return {}
```

## Authorization Status

Possible authorization statuses:

- **ACCEPTED** - Token is valid and authorized
- **BLOCKED** - Token is blocked
- **EXPIRED** - Token has expired
- **INVALID** - Token is invalid
- **CONCURRENT_TX** - Another transaction is active

## API Usage

### Authorize Token (POST)

```bash
curl -X POST 'http://127.0.0.1:8000/ocpi/emsp/2.3.0/tokens/CH/ABC/TOKEN123/authorize' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "location_id": "LOC001",
    "evse_uids": ["EVSE001"]
  }'
```

### Get Token (GET)

```bash
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/tokens/CH/ABC/TOKEN123' \
  -H 'Authorization: Token your-token'
```

### Create/Update Token (PUT)

```bash
curl -X PUT 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/tokens/CH/ABC/TOKEN123' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d @token.json
```

## Token Types

### RFID Card

```python
token_data = {
    "uid": "RFID123456",
    "type": "RFID",
    "auth_method": "AUTH_REQUEST"
}
```

### Mobile App

```python
token_data = {
    "uid": "APP_USER_123",
    "type": "APP_USER",
    "auth_method": "COMMAND"
}
```

### Other

```python
token_data = {
    "uid": "OTHER_TOKEN",
    "type": "OTHER",
    "auth_method": "WHITELIST"
}
```

## Whitelist Types

- **ALWAYS** - Token is always whitelisted
- **ALLOWED** - Token is allowed
- **ALLOWED_OFFLINE** - Token is allowed offline
- **NEVER** - Token is never whitelisted

## Best Practices

1. **Validate tokens** - Always check token validity
2. **Check expiration** - Verify token expiration dates
3. **Location access** - Verify token access to requested location
4. **Whitelist status** - Check whitelist status
5. **Log authorizations** - Log all authorization attempts

## Complete Example

See the [EMSP Sessions Example](../../examples/emsp_sessions/) which includes token authorization.
