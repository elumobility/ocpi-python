# EMSP Sessions Example

An eMobility Service Provider (EMSP) application that manages charging sessions and token authorization.

This example demonstrates:
- Setting up an EMSP application
- Managing charging sessions
- Token authorization
- Session lifecycle (start, update, stop)

## Running the Example

```bash
cd examples/emsp_sessions
uvicorn main:app --reload
```

## Testing

```bash
# Authorize a token
curl -X POST 'http://127.0.0.1:8000/ocpi/emsp/2.3.0/tokens/ES/ABC/TOKEN123/authorize' \
  -H 'Authorization: Token my-emsp-token-456' \
  -H 'Content-Type: application/json' \
  -d '{
    "location_id": "LOC001",
    "evse_uids": ["EVSE001"]
  }'

# Start a session
curl -X PUT 'http://127.0.0.1:8000/ocpi/emsp/2.3.0/sessions/ES/ABC/SESS001' \
  -H 'Authorization: Token my-emsp-token-456' \
  -H 'Content-Type: application/json' \
  -d @session.json

# Get all sessions
curl 'http://127.0.0.1:8000/ocpi/emsp/2.3.0/sessions/' \
  -H 'Authorization: Token my-emsp-token-456'
```
