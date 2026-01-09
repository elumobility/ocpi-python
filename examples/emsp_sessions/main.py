"""EMSP Sessions Example - eMobility Service Provider with Session Management.

This example demonstrates an EMSP setup with session and token management.
"""

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

from auth import SimpleAuthenticator
from crud import SimpleCrud

# Create the OCPI application
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.emsp],
    modules=[ModuleID.sessions, ModuleID.tokens],
    authenticator=SimpleAuthenticator,
    crud=SimpleCrud,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
