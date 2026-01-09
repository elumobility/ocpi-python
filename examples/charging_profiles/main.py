"""Charging Profiles Example - Smart Charging Control.

This example demonstrates charging profile management for smart charging.
"""

from auth import SimpleAuthenticator
from crud import SimpleCrud

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

# Create the OCPI application with charging profiles
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.charging_profile, ModuleID.sessions],
    authenticator=SimpleAuthenticator,
    crud=SimpleCrud,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
