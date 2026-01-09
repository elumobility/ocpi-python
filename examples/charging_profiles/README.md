# Charging Profiles Example

An example demonstrating smart charging with charging profiles (OCPI 2.2.1+).

This example demonstrates:
- Setting charging profiles
- Getting active charging profiles
- Clearing charging profiles
- Smart charging control

## Running the Example

```bash
cd examples/charging_profiles
uvicorn main:app --reload
```

## Testing

```bash
# Set a charging profile
curl -X PUT 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/chargingprofiles/SESS001' \
  -H 'Authorization: Token my-cpo-token-123' \
  -H 'Content-Type: application/json' \
  -d @charging_profile.json

# Get active charging profile
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/chargingprofiles/SESS001?duration=3600' \
  -H 'Authorization: Token my-cpo-token-123'
```
