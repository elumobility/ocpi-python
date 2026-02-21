"""EMSP routers for OCPI 2.3.0."""

from ocpi.core.enums import ModuleID
from ocpi.modules.bookings.v_2_3_0.api import (
    emsp_router as bookings_emsp_2_3_0_router,
)
from ocpi.modules.payments.v_2_3_0.api import (
    emsp_router as payments_emsp_2_3_0_router,
)
from ocpi.modules.cdrs.v_2_3_0.api import (
    emsp_router as cdrs_emsp_2_3_0_router,
)
from ocpi.modules.chargingprofiles.v_2_3_0.api import (
    emsp_router as chargingprofiles_emsp_2_3_0_router,
)
from ocpi.modules.commands.v_2_3_0.api import (
    emsp_router as commands_emsp_2_3_0_router,
)
from ocpi.modules.credentials.v_2_3_0.api import (
    emsp_router as credentials_emsp_2_3_0_router,
)
from ocpi.modules.hubclientinfo.v_2_3_0.api import (
    emsp_router as hubclientinfo_emsp_2_3_0_router,
)
from ocpi.modules.locations.v_2_3_0.api import (
    emsp_router as locations_emsp_2_3_0_router,
)
from ocpi.modules.sessions.v_2_3_0.api import (
    emsp_router as sessions_emsp_2_3_0_router,
)
from ocpi.modules.tariffs.v_2_3_0.api import (
    emsp_router as tariffs_emsp_2_3_0_router,
)
from ocpi.modules.tokens.v_2_3_0.api import (
    emsp_router as tokens_emsp_2_3_0_router,
)

router = {
    ModuleID.locations: locations_emsp_2_3_0_router,
    ModuleID.credentials_and_registration: credentials_emsp_2_3_0_router,
    ModuleID.sessions: sessions_emsp_2_3_0_router,
    ModuleID.commands: commands_emsp_2_3_0_router,
    ModuleID.tariffs: tariffs_emsp_2_3_0_router,
    ModuleID.tokens: tokens_emsp_2_3_0_router,
    ModuleID.cdrs: cdrs_emsp_2_3_0_router,
    ModuleID.hub_client_info: hubclientinfo_emsp_2_3_0_router,
    ModuleID.charging_profile: chargingprofiles_emsp_2_3_0_router,
    # New in OCPI 2.3.0
    ModuleID.bookings: bookings_emsp_2_3_0_router,
    ModuleID.payments: payments_emsp_2_3_0_router,
}
