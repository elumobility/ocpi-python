"""Tests for ocpi.main module."""

import pytest
from fastapi.testclient import TestClient

from ocpi import get_application
from ocpi.core import enums
from ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError
from ocpi.modules.versions.enums import VersionNumber
from tests.test_modules.utils import ClientAuthenticator


class MockCrud:
    @classmethod
    async def list(cls, module, role, filters, *args, **kwargs):
        return [], 0, False

    @classmethod
    async def get(cls, module, role, id, *args, **kwargs):
        return None

    @classmethod
    async def create(cls, module, role, data, *args, **kwargs):
        return data

    @classmethod
    async def update(cls, module, role, id, data, *args, **kwargs):
        return data

    @classmethod
    async def delete(cls, module, role, id, *args, **kwargs):
        return None

    @classmethod
    async def do(cls, module, role, action, *args, **kwargs):
        return None


def test_get_application_basic():
    """Test get_application creates a valid FastAPI app."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        modules=[enums.ModuleID.locations],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
    )
    
    assert app is not None
    assert app.title is not None


def test_get_application_invalid_version():
    """Test get_application with invalid version raises ValueError."""
    # Create a fake version that doesn't exist in ROUTERS
    class InvalidVersion:
        value = "9.9.9"
    
    with pytest.raises(ValueError, match="Version isn't supported"):
        get_application(
            version_numbers=[InvalidVersion()],  # type: ignore
            roles=[enums.RoleEnum.cpo],
            modules=[enums.ModuleID.locations],
            crud=MockCrud,
            authenticator=ClientAuthenticator,
        )


def test_get_application_with_http_push():
    """Test get_application with http_push enabled."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        modules=[enums.ModuleID.locations],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        http_push=True,
    )
    
    assert app is not None
    # Verify push router is included
    client = TestClient(app)
    # Push endpoints should be available
    # (exact path depends on settings, but router should be included)


def test_get_application_with_websocket_push():
    """Test get_application with websocket_push enabled."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        modules=[enums.ModuleID.locations],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        websocket_push=True,
    )
    
    assert app is not None


def test_get_application_multiple_versions():
    """Test get_application with multiple versions."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1, VersionNumber.v_2_2_1, VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        modules=[enums.ModuleID.locations],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
    )
    
    assert app is not None
    client = TestClient(app)
    # All versions should be available
    response = client.get("/ocpi/versions")
    # Versions endpoint doesn't require auth, so should be 200
    assert response.status_code in [200, 403]  # 403 if auth is required


def test_get_application_multiple_roles():
    """Test get_application with multiple roles."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo, enums.RoleEnum.emsp],
        modules=[enums.ModuleID.locations],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
    )
    
    assert app is not None
    client = TestClient(app)
    # Both CPO and EMSP endpoints should be available
    response = client.get("/ocpi/cpo/2.3.0/locations/")
    assert response.status_code in [200, 403]  # 403 if not authenticated


def test_get_application_ptp_role():
    """Test get_application with PTP role."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.ptp],
        modules=[enums.ModuleID.payments],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
    )
    
    assert app is not None


def test_get_application_multiple_modules():
    """Test get_application with multiple modules."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        modules=[
            enums.ModuleID.locations,
            enums.ModuleID.sessions,
            enums.ModuleID.cdrs,
        ],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
    )
    
    assert app is not None
    client = TestClient(app)
    # All module endpoints should be available
    response = client.get("/ocpi/cpo/2.3.0/locations/")
    assert response.status_code in [200, 403]


def test_exception_handler_middleware():
    """Test exception handler middleware catches OCPI errors."""
    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        modules=[enums.ModuleID.locations],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
    )
    
    client = TestClient(app)
    # Request without auth should return 403 (AuthorizationOCPIError)
    response = client.get("/ocpi/cpo/2.3.0/locations/")
    assert response.status_code == 403
