"""Full CPO Example - Complete Charge Point Operator Application.

This example demonstrates a full CPO setup with multiple modules:
- Locations
- Sessions
- CDRs
- Tariffs
- Commands
"""

from auth import SimpleAuthenticator
from crud import SimpleCrud

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

# Create the OCPI application with multiple modules
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[
        ModuleID.locations,
        ModuleID.sessions,
        ModuleID.cdrs,
        ModuleID.tariffs,
        ModuleID.commands,
    ],
    authenticator=SimpleAuthenticator,
    crud=SimpleCrud,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
