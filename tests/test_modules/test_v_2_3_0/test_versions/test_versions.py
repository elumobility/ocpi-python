from fastapi.testclient import TestClient

from ocpi.core import enums
from ocpi.core.crud import Crud
from ocpi.main import get_application
from ocpi.modules.versions.enums import VersionNumber
from tests.test_modules.test_v_2_3_0.test_versions.test_utils import (
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
)
from tests.test_modules.utils import AUTH_TOKEN, ClientAuthenticator

VERSIONS_URL = "/ocpi/versions"
VERSION_URL = "/ocpi/2.3.0/details"


def test_get_versions():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return AUTH_TOKEN

    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSIONS_URL,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_versions_not_authenticated():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return None

    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSIONS_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 401


def test_get_versions_v_2_3_0():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return AUTH_TOKEN

    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSION_URL,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_versions_v_2_3_0_not_authenticated():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return None

    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSION_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 401


def test_get_versions_without_auth_when_optional(monkeypatch):
    """When VERSIONS_REQUIRE_AUTH=False, /versions works without Authorization header."""
    monkeypatch.setattr("ocpi.core.config.settings.VERSIONS_REQUIRE_AUTH", False)

    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return None

    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(VERSIONS_URL)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_version_details_without_auth_when_optional(monkeypatch):
    """When VERSIONS_REQUIRE_AUTH=False, /2.3.0/details works without Authorization header."""
    monkeypatch.setattr("ocpi.core.config.settings.VERSIONS_REQUIRE_AUTH", False)

    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return None

    app = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(VERSION_URL)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 2
