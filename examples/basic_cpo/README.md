# Basic CPO Example

A simple Charge Point Operator (CPO) application that manages charging locations.

This example demonstrates:
- Setting up a basic OCPI CPO application
- Managing locations with CRUD operations
- Simple in-memory storage (replace with a database in production)

## Running the Example

```bash
cd examples/basic_cpo
uvicorn main:app --reload
```

## Testing

```bash
# Get available versions
curl http://127.0.0.1:8000/ocpi/versions

# Note: CPO locations are read-only via OCPI.
# Locations are managed in your own system and exposed through OCPI.
# The example includes a pre-populated location for demonstration.

# Get all locations
# Note: For OCPI 2.3.0, tokens must be base64-encoded
# Encode the token: echo -n "my-cpo-token-123" | base64
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/' \
  -H 'Authorization: Token bXktY3BvLXRva2VuLTEyMw=='

# Get all sessions
# Note: CPO only has a list endpoint, not individual session GET
# To get a specific session, use the list endpoint and filter by ID
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/sessions/' \
  -H 'Authorization: Token bXktY3BvLXRva2VuLTEyMw=='
```
