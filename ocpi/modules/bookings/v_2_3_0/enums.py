"""Enums for OCPI 2.3.0 Bookings module.

https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_bookings.asciidoc
"""

from enum import Enum


class BookingState(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_bookings.asciidoc#bookingstate-enum
    The state of a booking.
    """

    # The booking has been created/requested but not yet confirmed.
    pending = "PENDING"
    # The booking has been confirmed by the CPO.
    confirmed = "CONFIRMED"
    # The booking is currently active (charging session in progress).
    active = "ACTIVE"
    # The booking has been completed successfully.
    completed = "COMPLETED"
    # The booking has been cancelled by the EMSP.
    cancelled = "CANCELLED"
    # The booking has expired without being used.
    expired = "EXPIRED"
    # The booking has been rejected by the CPO.
    rejected = "REJECTED"
    # The booking could not be fulfilled (e.g., EVSE unavailable).
    failed = "FAILED"


class BookingResponseType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_bookings.asciidoc#bookingresponsetype-enum
    Response type for booking operations.
    """

    # The booking request has been accepted.
    accepted = "ACCEPTED"
    # The booking request has been rejected.
    rejected = "REJECTED"
    # The requested EVSE is not available for booking.
    evse_not_available = "EVSE_NOT_AVAILABLE"
    # The requested time slot is not available.
    time_slot_not_available = "TIME_SLOT_NOT_AVAILABLE"
    # The booking feature is not supported by this CPO.
    not_supported = "NOT_SUPPORTED"
    # Unknown error occurred.
    unknown_error = "UNKNOWN_ERROR"
