"""OCPI 2.3.0 router configuration."""

from ocpi.modules.versions import versions_v_2_3_0_router
from ocpi.routers import v_2_3_0_cpo_router, v_2_3_0_emsp_router, v_2_3_0_ptp_router

ROUTERS_DICT = {
    "version_router": versions_v_2_3_0_router,
    "cpo_router": v_2_3_0_cpo_router,
    "emsp_router": v_2_3_0_emsp_router,
    "ptp_router": v_2_3_0_ptp_router,
}
