from ocpi.core.endpoints.v_2_2_1.utils import cpo_generator
from ocpi.core.enums import ModuleID
from ocpi.modules.versions.v_2_2_1.schemas import InterfaceRole

CREDENTIALS_AND_REGISTRATION = cpo_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
    InterfaceRole.receiver,
)

CREDENTIALS_SENDER = cpo_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
    InterfaceRole.sender,
)

LOCATIONS = cpo_generator.generate_endpoint(
    ModuleID.locations,
    InterfaceRole.sender,
)

SESSIONS = cpo_generator.generate_endpoint(
    ModuleID.sessions,
    InterfaceRole.sender,
)

CDRS = cpo_generator.generate_endpoint(
    ModuleID.cdrs,
    InterfaceRole.sender,
)

TARIFFS = cpo_generator.generate_endpoint(
    ModuleID.tariffs,
    InterfaceRole.sender,
)

TOKENS = cpo_generator.generate_endpoint(
    ModuleID.tokens,
    InterfaceRole.receiver,
)

COMMANDS = cpo_generator.generate_endpoint(
    ModuleID.commands,
    InterfaceRole.receiver,
)

HUB_CLIENT_INFO = cpo_generator.generate_endpoint(
    ModuleID.hub_client_info,
    InterfaceRole.receiver,
)

CHARGING_PROFILE = cpo_generator.generate_endpoint(
    ModuleID.charging_profile,
    InterfaceRole.receiver,
)


ENDPOINTS_LIST = [
    CREDENTIALS_AND_REGISTRATION,
    CREDENTIALS_SENDER,
    LOCATIONS,
    SESSIONS,
    CDRS,
    TARIFFS,
    TOKENS,
    COMMANDS,
    HUB_CLIENT_INFO,
    CHARGING_PROFILE,
]
