from ocpi.core.endpoints.v_2_1_1.utils import cpo_generator
from ocpi.core.enums import ModuleID
from ocpi.modules.versions.v_2_1_1.schemas import Endpoint

# OCPI 2.1.1 Endpoint schema has no InterfaceRole field; credentials SENDER
# role is implicit and not separately advertised (InterfaceRole is 2.2.1+).

CREDENTIALS_AND_REGISTRATION = cpo_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
)

LOCATIONS = cpo_generator.generate_endpoint(ModuleID.locations)

CDRS = cpo_generator.generate_endpoint(ModuleID.cdrs)

TARIFFS = cpo_generator.generate_endpoint(ModuleID.tariffs)

SESSIONS = cpo_generator.generate_endpoint(ModuleID.sessions)

TOKENS = cpo_generator.generate_endpoint(ModuleID.tokens)

COMMANDS = cpo_generator.generate_endpoint(ModuleID.commands)

ENDPOINTS_LIST: list[Endpoint] = [
    CREDENTIALS_AND_REGISTRATION,
    LOCATIONS,
    CDRS,
    TARIFFS,
    SESSIONS,
    TOKENS,
    COMMANDS,
]
