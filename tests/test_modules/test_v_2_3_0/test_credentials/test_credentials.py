from typing import Any
from unittest.mock import patch

import pytest
from httpx import ASGITransport, AsyncClient

from py_ocpi.core import enums
from py_ocpi.core.config import settings
from py_ocpi.core.data_types import URL
from py_ocpi.core.dependencies import get_versions
from py_ocpi.main import get_application
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.schemas import Version

from .utils import (
    AUTH_HEADERS,
    CPO_BASE_URL,
    CREDENTIALS_TOKEN_CREATE,
    WRONG_AUTH_HEADERS,
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
@patch("py_ocpi.modules.credentials.v_2_3_0.api.cpo.httpx.AsyncClient")
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

    async with AsyncClient(
        transport=ASGITransport(app=app_2), base_url="http://test"
    ) as client:
        response = await client.post(
            CPO_BASE_URL,
            json=CREDENTIALS_TOKEN_CREATE,
            headers=AUTH_HEADERS,
        )

        assert response.status_code == 200
        assert "data" in response.json()


@pytest.mark.asyncio
async def test_cpo_get_credentials_v_2_3_0(app_1):
    async with AsyncClient(
        transport=ASGITransport(app=app_1), base_url="http://test"
    ) as client:
        response = await client.get(CPO_BASE_URL, headers=AUTH_HEADERS)

        assert response.status_code == 200
        assert "data" in response.json()
        assert "token" in response.json()["data"]


@pytest.mark.asyncio
async def test_cpo_post_credentials_not_authenticated_v_2_3_0(app_1):
    async with AsyncClient(
        transport=ASGITransport(app=app_1), base_url="http://test"
    ) as client:
        response = await client.post(
            CPO_BASE_URL,
            json=CREDENTIALS_TOKEN_CREATE,
            headers=WRONG_AUTH_HEADERS,
        )

        assert response.status_code == 403
