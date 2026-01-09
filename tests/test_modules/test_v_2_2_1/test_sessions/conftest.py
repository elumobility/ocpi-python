import pytest
from fastapi.testclient import TestClient

from ocpi.core import enums
from ocpi.main import get_application
from ocpi.modules.versions.enums import VersionNumber

from tests.test_modules.utils import ClientAuthenticator
from .utils import Crud


@pytest.fixture
def session_cpo_v_2_2_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.sessions],
    )


@pytest.fixture
def session_emsp_v_2_2_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.sessions],
    )


@pytest.fixture
def client_cpo_v_2_2_1(session_cpo_v_2_2_1):
    return TestClient(session_cpo_v_2_2_1)


@pytest.fixture
def client_emsp_v_2_2_1(session_emsp_v_2_2_1):
    return TestClient(session_emsp_v_2_2_1)
