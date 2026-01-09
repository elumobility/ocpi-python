"""OCPI 2.3.0 Bookings module.

New in OCPI 2.3.0 - Booking extension for EV charging reservations.
"""

from ocpi.modules.bookings.v_2_3_0.enums import BookingState
from ocpi.modules.bookings.v_2_3_0.schemas import (
    Booking,
    BookingPartialUpdate,
    BookingResponse,
)

__all__ = [
    "Booking",
    "BookingPartialUpdate",
    "BookingResponse",
    "BookingState",
]
