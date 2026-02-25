from ocpi.core.endpoints.v_2_1_1.utils import emsp_generator
from ocpi.core.enums import ModuleID
from ocpi.modules.versions.v_2_1_1.schemas import Endpoint

CREDENTIALS_AND_REGISTRATION = emsp_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
)

LOCATIONS = emsp_generator.generate_endpoint(ModuleID.locations)

CDRS = emsp_generator.generate_endpoint(ModuleID.cdrs)

TARIFFS = emsp_generator.generate_endpoint(ModuleID.tariffs)

SESSIONS = emsp_generator.generate_endpoint(ModuleID.sessions)

TOKENS = emsp_generator.generate_endpoint(ModuleID.tokens)

COMMANDS = emsp_generator.generate_endpoint(ModuleID.commands)

ENDPOINTS_LIST: list[Endpoint] = [
    CREDENTIALS_AND_REGISTRATION,
    LOCATIONS,
    CDRS,
    TARIFFS,
    SESSIONS,
    TOKENS,
    COMMANDS,
]
