"""OCPI 2.3.0 Bookings API."""

from ocpi.modules.bookings.v_2_3_0.api.cpo import router as cpo_router
from ocpi.modules.bookings.v_2_3_0.api.emsp import router as emsp_router

__all__ = ["cpo_router", "emsp_router"]
