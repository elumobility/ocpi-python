"""PTP routers for OCPI 2.3.0."""

from ocpi.core.enums import ModuleID
from ocpi.modules.payments.v_2_3_0.api import (
    ptp_router as payments_ptp_2_3_0_router,
)

router = {
    # New in OCPI 2.3.0
    ModuleID.payments: payments_ptp_2_3_0_router,
}
