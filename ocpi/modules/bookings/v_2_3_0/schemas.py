"""Schemas for OCPI 2.3.0 Bookings module.

New in OCPI 2.3.0 - Booking extension for EV charging reservations.
https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_bookings.asciidoc
"""

from pydantic import BaseModel

from ocpi.core.data_types import CiString, DateTime, DisplayText, Number, Price
from ocpi.modules.bookings.v_2_3_0.enums import BookingResponseType, BookingState
from ocpi.modules.tokens.v_2_3_0.schemas import Token


class Booking(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_bookings.asciidoc#booking-object
    Represents a booking for an EV charging session.
    """

    # CPO's country code (ISO-3166 alpha-2)
    country_code: CiString(2)  # type: ignore
    # CPO's party ID (following eMI3 standard)
    party_id: CiString(3)  # type: ignore
    # Unique identifier of the booking within the CPO's system
    id: CiString(36)  # type: ignore
    # Reference to the EMSP's booking request (for correlation)
    emsp_booking_id: CiString(36) | None = None  # type: ignore
    # Token used for this booking
    token: Token
    # ID of the Location where the booking is made
    location_id: CiString(36)  # type: ignore
    # ID of the EVSE where the booking is made (optional, can be any EVSE at location)
    evse_uid: CiString(36) | None = None  # type: ignore
    # ID of the specific connector (optional)
    connector_id: CiString(36) | None = None  # type: ignore
    # Start time of the booking
    start_date_time: DateTime
    # End time of the booking
    end_date_time: DateTime
    # Current state of the booking
    state: BookingState
    # Authorization reference (from EMSP)
    authorization_reference: CiString(36) | None = None  # type: ignore
    # Estimated energy to be delivered during this booking (in kWh)
    energy_estimate: Number | None = None
    # Estimated cost of this booking
    estimated_cost: Price | None = None
    # Human-readable message about the booking status
    status_message: list[DisplayText] = []
    # Reference to the session ID if booking has been converted to session
    session_id: CiString(36) | None = None  # type: ignore
    # Timestamp when this booking was last updated
    last_updated: DateTime


class BookingPartialUpdate(BaseModel):
    """Partial update schema for Booking object."""

    country_code: CiString(2) | None = None  # type: ignore
    party_id: CiString(3) | None = None  # type: ignore
    id: CiString(36) | None = None  # type: ignore
    emsp_booking_id: CiString(36) | None = None  # type: ignore
    token: Token | None = None
    location_id: CiString(36) | None = None  # type: ignore
    evse_uid: CiString(36) | None = None  # type: ignore
    connector_id: CiString(36) | None = None  # type: ignore
    start_date_time: DateTime | None = None
    end_date_time: DateTime | None = None
    state: BookingState | None = None
    authorization_reference: CiString(36) | None = None  # type: ignore
    energy_estimate: Number | None = None
    estimated_cost: Price | None = None
    status_message: list[DisplayText] | None = None
    session_id: CiString(36) | None = None  # type: ignore
    last_updated: DateTime | None = None


class BookingRequest(BaseModel):
    """
    Request object for creating a new booking.
    Sent by EMSP to CPO.
    """

    # EMSP's reference for this booking request
    emsp_booking_id: CiString(36)  # type: ignore
    # Token to be used for this booking
    token: Token
    # ID of the Location where the booking should be made
    location_id: CiString(36)  # type: ignore
    # ID of the preferred EVSE (optional)
    evse_uid: CiString(36) | None = None  # type: ignore
    # ID of the preferred connector (optional)
    connector_id: CiString(36) | None = None  # type: ignore
    # Requested start time
    start_date_time: DateTime
    # Requested end time
    end_date_time: DateTime
    # Authorization reference from EMSP
    authorization_reference: CiString(36) | None = None  # type: ignore
    # Estimated energy needed (in kWh)
    energy_estimate: Number | None = None


class BookingResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_bookings.asciidoc#bookingresponse-object
    Response to a booking request.
    """

    # Result of the booking request
    result: BookingResponseType
    # The booking object (if accepted)
    booking: Booking | None = None
    # Human-readable message about the response
    message: list[DisplayText] = []


class BookingCancelRequest(BaseModel):
    """Request to cancel a booking."""

    # Reason for cancellation
    reason: list[DisplayText] = []
