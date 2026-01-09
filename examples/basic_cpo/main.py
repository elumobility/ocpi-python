"""Basic CPO Example - Simple Charge Point Operator Application.

This example demonstrates a minimal CPO setup with location management.
"""

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber

from auth import SimpleAuthenticator
from crud import SimpleCrud

# Create the OCPI application
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.locations],
    authenticator=SimpleAuthenticator,
    crud=SimpleCrud,
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
