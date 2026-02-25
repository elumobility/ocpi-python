"""EMSP endpoints for OCPI 2.3.0."""

from ocpi.core.endpoints.v_2_3_0.utils import emsp_generator
from ocpi.core.enums import ModuleID
from ocpi.modules.versions.v_2_3_0.schemas import Endpoint, InterfaceRole

# eMSP advertises credentials as RECEIVER only. Adding credentials SENDER would
# allow the eMSP to push proactive credential updates to registered CPOs, but
# this is not required for current integrations (Payter, etc.). Add
# CREDENTIALS_SENDER here if an eMSP-initiated credential update flow is needed.
CREDENTIALS_AND_REGISTRATION = emsp_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
    InterfaceRole.receiver,
)

LOCATIONS = emsp_generator.generate_endpoint(
    ModuleID.locations,
    InterfaceRole.receiver,
)

SESSIONS = emsp_generator.generate_endpoint(
    ModuleID.sessions,
    InterfaceRole.receiver,
)

CDRS = emsp_generator.generate_endpoint(
    ModuleID.cdrs,
    InterfaceRole.receiver,
)

TARIFFS = emsp_generator.generate_endpoint(
    ModuleID.tariffs,
    InterfaceRole.receiver,
)

TOKENS = emsp_generator.generate_endpoint(
    ModuleID.tokens,
    InterfaceRole.sender,
)

COMMANDS = emsp_generator.generate_endpoint(
    ModuleID.commands,
    InterfaceRole.sender,
)

HUB_CLIENT_INFO = emsp_generator.generate_endpoint(
    ModuleID.hub_client_info,
    InterfaceRole.receiver,
)

CHARGING_PROFILE = emsp_generator.generate_endpoint(
    ModuleID.charging_profile,
    InterfaceRole.sender,
)

# New in OCPI 2.3.0 - Booking extension
BOOKINGS = emsp_generator.generate_endpoint(
    ModuleID.bookings,
    InterfaceRole.receiver,
)


ENDPOINTS_LIST: list[Endpoint] = [
    CREDENTIALS_AND_REGISTRATION,
    LOCATIONS,
    SESSIONS,
    CDRS,
    TARIFFS,
    TOKENS,
    COMMANDS,
    HUB_CLIENT_INFO,
    CHARGING_PROFILE,
    BOOKINGS,
]
