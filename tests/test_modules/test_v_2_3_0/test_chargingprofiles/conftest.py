import pytest
from fastapi.testclient import TestClient

from ocpi.core import enums
from ocpi.main import get_application
from ocpi.modules.versions.enums import VersionNumber

from .utils import ClientAuthenticator, Crud


@pytest.fixture
def charging_profile_cpo_v_2_3_0():
    return get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.charging_profile],
    )


@pytest.fixture
def charging_profile_emsp_v_2_3_0():
    return get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.charging_profile],
    )


@pytest.fixture
def client_cpo_v_2_3_0(charging_profile_cpo_v_2_3_0):
    return TestClient(charging_profile_cpo_v_2_3_0)


@pytest.fixture
def client_emsp_v_2_3_0(charging_profile_emsp_v_2_3_0):
    return TestClient(charging_profile_emsp_v_2_3_0)
