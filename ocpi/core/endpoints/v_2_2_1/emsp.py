from ocpi.core.endpoints.v_2_2_1.utils import emsp_generator
from ocpi.core.enums import ModuleID
from ocpi.modules.versions.v_2_2_1.schemas import Endpoint, InterfaceRole

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

COMMANDS = emsp_generator.generate_endpoint(
    ModuleID.commands,
    InterfaceRole.sender,
)

TOKENS = emsp_generator.generate_endpoint(
    ModuleID.tokens,
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

ENDPOINTS_LIST: list[Endpoint] = [
    CREDENTIALS_AND_REGISTRATION,
    LOCATIONS,
    SESSIONS,
    CDRS,
    TARIFFS,
    COMMANDS,
    TOKENS,
    HUB_CLIENT_INFO,
    CHARGING_PROFILE,
]
