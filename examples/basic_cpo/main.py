"""Basic CPO Example - Simple Charge Point Operator Application.

This example demonstrates a minimal CPO setup with location management.
"""

import traceback
from auth import SimpleAuthenticator
from crud import SimpleCrud

from ocpi import get_application
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError
from ocpi.modules.versions.enums import VersionNumber
from pydantic import ValidationError

# Monkey patch the exception handler to print full tracebacks
import ocpi.main

# Store original dispatch
_original_dispatch = ocpi.main.ExceptionHandlerMiddleware.dispatch


async def _debug_dispatch(self, request, call_next):
    try:
        response = await call_next(request)
        return response
    except AuthorizationOCPIError as e:
        print(f"\n{'='*60}")
        print(f"AUTHORIZATION ERROR: {e}")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise
    except NotFoundOCPIError as e:
        print(f"\n{'='*60}")
        print(f"NOT FOUND ERROR: {e}")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise
    except ValidationError as e:
        print(f"\n{'='*60}")
        print(f"VALIDATION ERROR: {e}")
        print(f"ValidationError details: {str(e)}")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"UNKNOWN EXCEPTION: {type(e).__name__}: {e}")
        print(f"Full traceback:")
        traceback.print_exc()
        print(f"{'='*60}\n")
        raise


ocpi.main.ExceptionHandlerMiddleware.dispatch = _debug_dispatch

# Create the OCPI application
app = get_application(
    version_numbers=[VersionNumber.v_2_3_0],
    roles=[RoleEnum.cpo],
    modules=[ModuleID.locations, ModuleID.sessions],  # Added sessions module
    authenticator=SimpleAuthenticator,
    crud=SimpleCrud,
)

if __name__ == "__main__":
    import uvicorn

    # Note: reload=True only works when running uvicorn as a command, not with uvicorn.run()
    # To use reload, run: uvicorn main:app --reload --port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
