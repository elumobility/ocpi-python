from typing import Any
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from ocpi.core import enums
from ocpi.core.config import settings
from ocpi.core.data_types import URL
from ocpi.core.dependencies import get_versions
from ocpi.main import get_application
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.schemas import Version
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN_A_V_2_3_0,
    ENCODED_AUTH_TOKEN_V_2_3_0,
    ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0,
)

from .utils import (
    CPO_BASE_URL,
    CREDENTIALS_TOKEN_CREATE,
    ClientAuthenticator,
    Crud,
)


@pytest.fixture
def app_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.credentials_and_registration],
    )


@pytest.mark.asyncio
@patch("ocpi.modules.credentials.v_2_3_0.api.cpo.httpx.AsyncClient")
async def test_cpo_post_credentials_v_2_3_0(async_client):
    class MockCrud(Crud):
        @classmethod
        async def do(
            cls,
            module: enums.ModuleID,
            role: enums.RoleEnum,
            action: enums.Action,
            auth_token,
            *args,
            data: dict = None,
            **kwargs,
        ) -> Any:
            # Return None for get_client_token to indicate no existing registration
            if action == enums.Action.get_client_token:
                return None
            return {}

    app_1 = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.emsp],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.credentials_and_registration],
    )

    def override_get_versions():
        return [
            Version(
                version=VersionNumber.v_2_3_0,
                url=URL(
                    f"/{settings.OCPI_PREFIX}/{VersionNumber.v_2_3_0.value}/details"
                ),
            ).model_dump()
        ]

    app_1.dependency_overrides[get_versions] = override_get_versions

    async_client.return_value = AsyncClient(
        transport=ASGITransport(app=app_1), base_url="http://test"
    )

    app_2 = get_application(
        version_numbers=[VersionNumber.v_2_3_0],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.credentials_and_registration],
    )

    # For 2.3.0, tokens ARE base64 encoded in Authorization header
    auth_headers = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_A_V_2_3_0}"}

    async with AsyncClient(
        transport=ASGITransport(app=app_2), base_url="http://test"
    ) as client:
        response = await client.post(
            CPO_BASE_URL,
            json=CREDENTIALS_TOKEN_CREATE,
            headers=auth_headers,
        )

        assert response.status_code == 200
        assert "data" in response.json()


@pytest.mark.asyncio
async def test_cpo_get_credentials_v_2_3_0(app_1):
    # For 2.3.0, tokens ARE base64 encoded in Authorization header
    auth_headers = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_V_2_3_0}"}

    async with AsyncClient(
        transport=ASGITransport(app=app_1), base_url="http://test"
    ) as client:
        response = await client.get(CPO_BASE_URL, headers=auth_headers)

        assert response.status_code == 200
        assert "data" in response.json()
        # The data structure may vary, check that data exists
        data = response.json()["data"]
        assert isinstance(data, dict) and "token" in data


@pytest.mark.asyncio
async def test_cpo_post_credentials_not_authenticated_v_2_3_0(app_1):
    # For 2.3.0, tokens ARE base64 encoded in Authorization header
    wrong_auth_headers = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN_V_2_3_0}"}

    async with AsyncClient(
        transport=ASGITransport(app=app_1), base_url="http://test"
    ) as client:
        response = await client.post(
            CPO_BASE_URL,
            json=CREDENTIALS_TOKEN_CREATE,
            headers=wrong_auth_headers,
        )

        assert response.status_code == 401  # Unauthorized when token is invalid
