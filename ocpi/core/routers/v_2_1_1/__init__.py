from ocpi.modules.versions import versions_v_2_1_1_router
from ocpi.routers import v_2_1_1_cpo_router, v_2_1_1_emsp_router

ROUTERS_DICT = {
    "version_router": versions_v_2_1_1_router,
    "cpo_router": v_2_1_1_cpo_router,
    "emsp_router": v_2_1_1_emsp_router,
}
