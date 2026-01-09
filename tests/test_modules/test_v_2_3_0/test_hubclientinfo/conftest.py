import pytest

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.modules.versions.enums import VersionNumber

from .utils import Crud, ClientAuthenticator


@pytest.fixture
def hubclientinfo_cpo_v_2_3_0():
    return get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.hub_client_info],
    )


@pytest.fixture
def hubclientinfo_emsp_v_2_3_0():
    return get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.hub_client_info],
    )


@pytest.fixture
def client_cpo_v_2_3_0(hubclientinfo_cpo_v_2_3_0):
    return TestClient(hubclientinfo_cpo_v_2_3_0)


@pytest.fixture
def client_emsp_v_2_3_0(hubclientinfo_emsp_v_2_3_0):
    return TestClient(hubclientinfo_emsp_v_2_3_0)
