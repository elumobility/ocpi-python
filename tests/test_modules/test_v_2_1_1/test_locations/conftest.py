import pytest
from fastapi.testclient import TestClient

from ocpi.core import enums
from ocpi.main import get_application
from ocpi.modules.versions.enums import VersionNumber

from .utils import ClientAuthenticator, Crud


@pytest.fixture
def location_cpo_v_2_1_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.locations],
    )


@pytest.fixture
def location_emsp_v_2_1_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.locations],
    )


@pytest.fixture
def client_cpo_v_2_1_1(location_cpo_v_2_1_1):
    return TestClient(location_cpo_v_2_1_1)


@pytest.fixture
def client_emsp_v_2_1_1(location_emsp_v_2_1_1):
    return TestClient(location_emsp_v_2_1_1)
