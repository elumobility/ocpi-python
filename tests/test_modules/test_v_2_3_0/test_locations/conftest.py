import pytest
from fastapi.testclient import TestClient

from ocpi.core import enums
from ocpi.main import get_application
from ocpi.modules.versions.enums import VersionNumber

from tests.test_modules.utils import ClientAuthenticator
from .utils import Crud


@pytest.fixture
def location_cpo_v_2_3_0():
    return get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.locations],
    )


@pytest.fixture
def location_emsp_v_2_3_0():
    return get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.locations],
    )


@pytest.fixture
def client_cpo_v_2_3_0(location_cpo_v_2_3_0):
    return TestClient(location_cpo_v_2_3_0)


@pytest.fixture
def client_emsp_v_2_3_0(location_emsp_v_2_3_0):
    return TestClient(location_emsp_v_2_3_0)
