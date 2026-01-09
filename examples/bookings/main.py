"""Bookings Example - OCPI 2.3.0 Booking Reservations.

This example demonstrates the OCPI 2.3.0 Booking extension for managing
EV charging reservations.
"""

from auth import SimpleAuthenticator
from crud import BookingsCrud

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

# Create the OCPI application with Bookings module
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.bookings],
    authenticator=SimpleAuthenticator,
    crud=BookingsCrud,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
