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

# Create a location
curl -X PUT 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/DE/ABC/LOC001' \
  -H 'Authorization: Token my-cpo-token-123' \
  -H 'Content-Type: application/json' \
  -d @location.json

# Get all locations
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/locations/' \
  -H 'Authorization: Token my-cpo-token-123'
```
