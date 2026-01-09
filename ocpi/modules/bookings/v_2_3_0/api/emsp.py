"""EMSP Bookings API for OCPI 2.3.0.

The EMSP creates booking requests and receives booking updates from CPOs.
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
from ocpi.core.status import OCPI_2003_UNKNOWN_RESOURCE
from ocpi.core.utils import get_list
from ocpi.modules.bookings.v_2_3_0.schemas import (
    Booking,
    BookingPartialUpdate,
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
    Get Bookings (EMSP).

    Retrieves bookings created by this EMSP.
    Supports pagination via date_from, date_to, offset, and limit parameters.

    **Returns:**
        OCPIResponse containing a list of Booking objects.
    """
    logger.info("Received request to get bookings (EMSP).")

    data_list = await get_list(
        response,
        filters,
        ModuleID.bookings,
        RoleEnum.emsp,
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


@router.get(
    "/{country_code}/{party_id}/{booking_id}",
    response_model=OCPIResponse,
)
async def get_booking(
    request: Request,
    country_code: str,
    party_id: str,
    booking_id: str,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Booking (EMSP).

    Retrieves a specific booking by country_code, party_id, and booking_id.

    **Path parameters:**
        - country_code: CPO's country code (ISO-3166 alpha-2).
        - party_id: CPO's party ID.
        - booking_id: The unique identifier of the booking.

    **Returns:**
        OCPIResponse containing the Booking object.
    """
    logger.info(
        f"Received request to get booking {country_code}/{party_id}/{booking_id} (EMSP)."
    )

    data = await crud.get(
        ModuleID.bookings,
        RoleEnum.emsp,
        booking_id,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_3_0,
    )

    if data is None:
        # OCPI uses 2003 for any "resource not found" scenario
        return OCPIResponse(
            data=[],
            **OCPI_2003_UNKNOWN_RESOURCE,
        )

    return OCPIResponse(
        data=adapter.booking_adapter(data, VersionNumber.v_2_3_0).model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put(
    "/{country_code}/{party_id}/{booking_id}",
    response_model=OCPIResponse,
)
async def add_or_update_booking(
    request: Request,
    country_code: str,
    party_id: str,
    booking_id: str,
    booking: Booking,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Booking (EMSP).

    CPO pushes a new booking or updates an existing one.

    **Path parameters:**
        - country_code: CPO's country code (ISO-3166 alpha-2).
        - party_id: CPO's party ID.
        - booking_id: The unique identifier of the booking.

    **Request body:**
        Booking: The complete booking object.

    **Returns:**
        OCPIResponse containing the Booking object.
    """
    logger.info(
        f"Received request to add/update booking {country_code}/{party_id}/{booking_id} (EMSP)."
    )

    # Check if booking exists
    existing = await crud.get(
        ModuleID.bookings,
        RoleEnum.emsp,
        booking_id,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_3_0,
    )

    if existing:
        # Update existing booking
        data = await crud.update(
            ModuleID.bookings,
            RoleEnum.emsp,
            booking.model_dump(),
            booking_id,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_3_0,
        )
    else:
        # Create new booking
        data = await crud.create(
            ModuleID.bookings,
            RoleEnum.emsp,
            booking.model_dump(),
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_3_0,
        )

    return OCPIResponse(
        data=adapter.booking_adapter(data, VersionNumber.v_2_3_0).model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch(
    "/{country_code}/{party_id}/{booking_id}",
    response_model=OCPIResponse,
)
async def partial_update_booking(
    request: Request,
    country_code: str,
    party_id: str,
    booking_id: str,
    booking_update: BookingPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Partial Update Booking (EMSP).

    CPO pushes a partial update to an existing booking.

    **Path parameters:**
        - country_code: CPO's country code (ISO-3166 alpha-2).
        - party_id: CPO's party ID.
        - booking_id: The unique identifier of the booking.

    **Request body:**
        BookingPartialUpdate: The fields to update.

    **Returns:**
        OCPIResponse containing the updated Booking object.
    """
    logger.info(
        f"Received request to partial update booking {country_code}/{party_id}/{booking_id} (EMSP)."
    )

    data = await crud.update(
        ModuleID.bookings,
        RoleEnum.emsp,
        booking_update.model_dump(exclude_unset=True),
        booking_id,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_3_0,
    )

    if data is None:
        # OCPI uses 2003 for any "resource not found" scenario
        return OCPIResponse(
            data=[],
            **OCPI_2003_UNKNOWN_RESOURCE,
        )

    return OCPIResponse(
        data=adapter.booking_adapter(data, VersionNumber.v_2_3_0).model_dump(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.delete(
    "/{country_code}/{party_id}/{booking_id}",
    response_model=OCPIResponse,
)
async def delete_booking(
    request: Request,
    country_code: str,
    party_id: str,
    booking_id: str,
    crud: Crud = Depends(get_crud),
):
    """
    Delete Booking (EMSP).

    CPO notifies that a booking has been deleted/cancelled.

    **Path parameters:**
        - country_code: CPO's country code (ISO-3166 alpha-2).
        - party_id: CPO's party ID.
        - booking_id: The unique identifier of the booking.

    **Returns:**
        OCPIResponse confirming the deletion.
    """
    logger.info(
        f"Received request to delete booking {country_code}/{party_id}/{booking_id} (EMSP)."
    )

    await crud.delete(
        ModuleID.bookings,
        RoleEnum.emsp,
        booking_id,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_3_0,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
