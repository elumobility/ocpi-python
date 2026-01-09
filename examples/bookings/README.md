# Bookings Example

A CPO application that manages EV charging reservations using the OCPI 2.3.0 Booking extension.

This example demonstrates:
- Setting up an OCPI application with the Bookings module (new in OCPI 2.3.0)
- Managing booking reservations for charging stations
- Handling booking lifecycle (pending → confirmed → active → completed)
- Simple in-memory storage (replace with a database in production)

## Running the Example

```bash
cd examples/bookings
uvicorn main:app --reload
```

## API Endpoints

### CPO Endpoints (Receive booking requests from EMSPs)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/ocpi/cpo/2.3.0/bookings` | List all bookings |
| GET | `/ocpi/cpo/2.3.0/bookings/{id}` | Get specific booking |
| POST | `/ocpi/cpo/2.3.0/bookings` | Create new booking |
| PATCH | `/ocpi/cpo/2.3.0/bookings/{id}` | Update booking |
| DELETE | `/ocpi/cpo/2.3.0/bookings/{id}` | Cancel booking |

## Testing

```bash
# Get available versions
curl http://127.0.0.1:8000/ocpi/versions

# Create a booking (as EMSP sending to CPO)
curl -X POST 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/bookings' \
  -H 'Authorization: Token bXktY3BvLXRva2VuLTEyMw==' \
  -H 'Content-Type: application/json' \
  -d @booking.json

# Get all bookings
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/bookings' \
  -H 'Authorization: Token bXktY3BvLXRva2VuLTEyMw=='

# Get a specific booking
curl 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/bookings/BOOKING-001' \
  -H 'Authorization: Token bXktY3BvLXRva2VuLTEyMw=='

# Update booking state to active
curl -X PATCH 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/bookings/BOOKING-001' \
  -H 'Authorization: Token bXktY3BvLXRva2VuLTEyMw==' \
  -H 'Content-Type: application/json' \
  -d '{"state": "ACTIVE"}'

# Cancel a booking
curl -X DELETE 'http://127.0.0.1:8000/ocpi/cpo/2.3.0/bookings/BOOKING-001' \
  -H 'Authorization: Token bXktY3BvLXRva2VuLTEyMw=='
```

## Booking States

| State | Description |
|-------|-------------|
| `PENDING` | Booking created but not yet confirmed |
| `CONFIRMED` | Booking confirmed by CPO |
| `ACTIVE` | Charging session in progress |
| `COMPLETED` | Booking completed successfully |
| `CANCELLED` | Booking cancelled |
| `EXPIRED` | Booking expired without being used |
| `REJECTED` | Booking rejected by CPO |
| `FAILED` | Booking could not be fulfilled |

## Notes

- The `Authorization` header must be Base64-encoded for OCPI 2.3.0
- `bXktY3BvLXRva2VuLTEyMw==` is Base64 encoding of `my-cpo-token-123`
- In production, use proper token management and database storage
