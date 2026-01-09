"""CPO Bookings API for OCPI 2.3.0.

The CPO receives booking requests from EMSPs and manages booking lifecycle.
"""

from fastapi import APIRouter, Depends, Request, Response

from ocpi.core import status
from ocpi.core.adapter import Adapter
from ocpi.core.authentication.verifier import AuthorizationVerifier
from ocpi.core.config import logger
from ocpi.core.crud import Crud
from ocpi.core.dependencies import get_adapter, get_crud, pagination_filters
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.schemas import OCPIResponse
from ocpi.core.utils import get_list
from ocpi.modules.bookings.v_2_3_0.enums import BookingResponseType
from ocpi.modules.bookings.v_2_3_0.schemas import (
    BookingCancelRequest,
    BookingPartialUpdate,
    BookingRequest,
    BookingResponse,
)
from ocpi.modules.versions.enums import VersionNumber

router = APIRouter(
    prefix="/bookings",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_3_0))],
)


@router.get("", response_model=OCPIResponse)
async def get_bookings(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get Bookings (CPO).

    Retrieves a list of bookings owned by this CPO.
    Supports pagination via date_from, date_to, offset, and limit parameters.

    **Returns:**
        OCPIResponse containing a list of Booking objects.
    """
    logger.info("Received request to get bookings (CPO).")

    data_list = await get_list(
        response,
        filters,
        ModuleID.bookings,
        RoleEnum.cpo,
        VersionNumber.v_2_3_0,
        crud,
    )

    bookings = []
    for data in data_list:
        bookings.append(
            adapter.booking_adapter(data, VersionNumber.v_2_3_0).model_dump()
        )
    logger.debug(f"Amount of bookings in response: {len(bookings)}")

    return OCPIResponse(
        data=bookings,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.get("/{booking_id}", response_model=OCPIResponse)
async def get_booking(
    request: Request,
    booking_id: str,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Booking (CPO).

    Retrieves a specific booking by ID.

    **Path parameters:**
        - booking_id: The unique identifier of the booking.

    **Returns:**
        OCPIResponse containing the Booking object.
    """
    logger.info(f"Received request to get booking {booking_id} (CPO).")

    data = await crud.get(
        ModuleID.bookings,
        RoleEnum.cpo,
        booking_id,
        version=VersionNumber.v_2_3_0,
    )

    if data is None:
        return OCPIResponse(
            data=[],
            **status.OCPI_2003_UNKNOWN_LOCATION,
        )

    return OCPIResponse(
        data=adapter.booking_adapter(data, VersionNumber.v_2_3_0).model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("", response_model=OCPIResponse)
async def create_booking(
    request: Request,
    booking_request: BookingRequest,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Create Booking (CPO).

    Receives a booking request from an EMSP and creates a new booking.

    **Request body:**
        BookingRequest: The booking request details.

    **Returns:**
        OCPIResponse containing a BookingResponse object.
    """
    logger.info("Received booking request (CPO).")
    logger.debug(f"Booking request: {booking_request.model_dump()}")

    # Process the booking request via CRUD
    result = await crud.create(
        ModuleID.bookings,
        RoleEnum.cpo,
        booking_request.model_dump(),
        version=VersionNumber.v_2_3_0,
    )

    if result is None:
        booking_response = BookingResponse(
            result=BookingResponseType.unknown_error,
            message=[],
        )
    else:
        booking = adapter.booking_adapter(result, VersionNumber.v_2_3_0)
        booking_response = BookingResponse(
            result=BookingResponseType.accepted,
            booking=booking,
        )

    return OCPIResponse(
        data=booking_response.model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch("/{booking_id}", response_model=OCPIResponse)
async def update_booking(
    request: Request,
    booking_id: str,
    booking_update: BookingPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Update Booking (CPO).

    Partially updates an existing booking.

    **Path parameters:**
        - booking_id: The unique identifier of the booking.

    **Request body:**
        BookingPartialUpdate: The fields to update.

    **Returns:**
        OCPIResponse containing the updated Booking object.
    """
    logger.info(f"Received request to update booking {booking_id} (CPO).")

    data = await crud.update(
        ModuleID.bookings,
        RoleEnum.cpo,
        booking_update.model_dump(exclude_unset=True),
        booking_id,
        version=VersionNumber.v_2_3_0,
    )

    if data is None:
        return OCPIResponse(
            data=[],
            **status.OCPI_2003_UNKNOWN_LOCATION,
        )

    return OCPIResponse(
        data=adapter.booking_adapter(data, VersionNumber.v_2_3_0).model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.delete("/{booking_id}", response_model=OCPIResponse)
async def cancel_booking(
    request: Request,
    booking_id: str,
    cancel_request: BookingCancelRequest | None = None,
    crud: Crud = Depends(get_crud),
):
    """
    Cancel Booking (CPO).

    Cancels an existing booking.

    **Path parameters:**
        - booking_id: The unique identifier of the booking.

    **Request body (optional):**
        BookingCancelRequest: Reason for cancellation.

    **Returns:**
        OCPIResponse confirming the cancellation.
    """
    logger.info(f"Received request to cancel booking {booking_id} (CPO).")

    await crud.delete(
        ModuleID.bookings,
        RoleEnum.cpo,
        booking_id,
        version=VersionNumber.v_2_3_0,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
