"""SCSP routers for OCPI 2.2.1.

The SCSP (Smart Charging Service Provider) is a *receiver* of Sessions and
ChargingProfiles, so it reuses the eMSP receiver-side module routers (the
receiver interface is identical). Mounted under the ``/scsp/`` prefix by
``get_application``.
"""

from ocpi.core.enums import ModuleID
from ocpi.modules.chargingprofiles.v_2_2_1.api import (
    emsp_router as chargingprofiles_emsp_2_2_1_router,
)
from ocpi.modules.sessions.v_2_2_1.api import (
    emsp_router as sessions_emsp_2_2_1_router,
)

router = {
    ModuleID.sessions: sessions_emsp_2_2_1_router,
    ModuleID.charging_profile: chargingprofiles_emsp_2_2_1_router,
}
