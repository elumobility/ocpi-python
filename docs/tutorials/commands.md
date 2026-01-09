# Commands

This tutorial demonstrates how to send commands to charge points in an OCPI application.

## Overview

Commands allow an EMSP to control charging sessions at a CPO's charge points:
- **START_SESSION** - Start a charging session
- **STOP_SESSION** - Stop an active session
- **RESERVE_NOW** - Reserve a connector
- **UNLOCK_CONNECTOR** - Unlock a connector

## Setup

Include the commands module:

```python
from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo, RoleEnum.emsp],
    modules=[ModuleID.commands],
    authenticator=YourAuthenticator,
    crud=YourCrud,
)
```

## Command Types

### START_SESSION

Start a charging session:

```python
command_data = {
    "response_url": "https://emsp.example.com/commands/response",
    "token": {
        "uid": "TOKEN123",
        "type": "RFID",
        "contract_id": "CONTRACT001"
    },
    "location_id": "LOC001",
    "evse_uid": "EVSE001",
    "connector_id": "CONN001",
    "authorization_reference": "AUTH_REF_123"
}
```

### STOP_SESSION

Stop an active session:

```python
command_data = {
    "response_url": "https://emsp.example.com/commands/response",
    "session_id": "SESS001"
}
```

### RESERVE_NOW

Reserve a connector:

```python
command_data = {
    "response_url": "https://emsp.example.com/commands/response",
    "token": {
        "uid": "TOKEN123",
        "type": "RFID",
        "contract_id": "CONTRACT001"
    },
    "expiry_date": "2024-01-01T12:00:00Z",
    "reservation_id": "RES001",
    "location_id": "LOC001",
    "evse_id": "EVSE001",
    "connector_id": "CONN001",
    "authorization_reference": "AUTH_REF_123"
}
```

### UNLOCK_CONNECTOR

Unlock a connector:

```python
command_data = {
    "response_url": "https://emsp.example.com/commands/response",
    "location_id": "LOC001",
    "evse_id": "EVSE001",
    "connector_id": "CONN001"
}
```

## Implementing Command Handling

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
        """Handle command execution."""
        if module == ModuleID.commands:
            command = kwargs.get("command")
            response_url = data.get("response_url") if data else None
            
            # Send command to charge point via OCPP
            # This is a simplified example
            if command == "START_SESSION":
                # Send OCPP RemoteStartTransaction
                result = await send_ocpp_command("RemoteStartTransaction", {
                    "idTag": data.get("token", {}).get("uid"),
                    "connectorId": data.get("connector_id")
                })
                
                return {
                    "result": "ACCEPTED" if result else "REJECTED",
                    "timeout": 30
                }
            
            elif command == "STOP_SESSION":
                # Send OCPP RemoteStopTransaction
                result = await send_ocpp_command("RemoteStopTransaction", {
                    "transactionId": data.get("session_id")
                })
                
                return {
                    "result": "ACCEPTED" if result else "REJECTED",
                    "timeout": 30
                }
            
            # ... handle other commands ...
        
        return {}
```

## Command Response

After executing a command, send the result to the `response_url`:

```python
async def send_command_response(response_url: str, result: dict):
    """Send command result to EMSP."""
    async with httpx.AsyncClient() as client:
        await client.post(response_url, json={
            "result": result.get("result"),
            "timeout": result.get("timeout")
        })
```

## Command Results

Possible command results:

- **ACCEPTED** - Command was accepted
- **CANCELED_RESERVATION** - Reservation was canceled
- **EVSE_OCCUPIED** - EVSE is occupied
- **FAILED** - Command failed
- **NOT_SUPPORTED** - Command not supported
- **REJECTED** - Command was rejected
- **TIMEOUT** - Command timed out
- **UNKNOWN_RESERVATION** - Reservation not found

## API Usage

### Send START_SESSION Command

```bash
curl -X POST 'http://127.0.0.1:8000/ocpi/emsp/2.3.0/commands/START_SESSION' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "response_url": "https://emsp.example.com/commands/response",
    "token": {
      "uid": "TOKEN123",
      "type": "RFID"
    },
    "location_id": "LOC001",
    "evse_uid": "EVSE001",
    "connector_id": "CONN001"
  }'
```

### Send STOP_SESSION Command

```bash
curl -X POST 'http://127.0.0.1:8000/ocpi/emsp/2.3.0/commands/STOP_SESSION' \
  -H 'Authorization: Token your-token' \
  -H 'Content-Type: application/json' \
  -d '{
    "response_url": "https://emsp.example.com/commands/response",
    "session_id": "SESS001"
  }'
```

## Best Practices

1. **Validate commands** - Check command parameters before execution
2. **Handle timeouts** - Set appropriate timeout values
3. **Send responses** - Always send command results to response_url
4. **Error handling** - Handle OCPP communication errors gracefully
5. **Log commands** - Log all command attempts and results
6. **Check EVSE status** - Verify EVSE availability before commands

## Complete Example

See the [Full CPO Example](../../examples/full_cpo/) which includes command handling.
