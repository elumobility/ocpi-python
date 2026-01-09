from typing import Any
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.core.config import settings
from py_ocpi.core.data_types import URL
from py_ocpi.core.dependencies import get_versions
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.schemas import Version
from tests.test_modules.utils import ClientAuthenticator

from .utils import (
    AUTH_HEADERS,
    AUTH_HEADERS_A,
    AUTH_TOKEN_A_V_2_2_1,
    CREDENTIALS_TOKEN_CREATE,
    Crud,
)


def test_cpo_get_credentials_v_2_2_1():
    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.credentials_and_registration],
    )

    client = TestClient(app)
    response = client.get(
        "/ocpi/cpo/2.2.1/credentials",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"]["token"] == AUTH_TOKEN_A_V_2_2_1


@pytest.mark.asyncio
@patch("py_ocpi.modules.credentials.v_2_2_1.api.cpo.httpx.AsyncClient")
async def test_cpo_post_credentials_v_2_2_1(async_client):
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
            return {}

    app_1 = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.emsp],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.credentials_and_registration],
    )

    def override_get_versions():
        return [
            Version(
                version=VersionNumber.v_2_2_1,
                url=URL(
                    f"/{settings.OCPI_PREFIX}/{VersionNumber.v_2_2_1.value}/details"
                ),
            ).model_dump()
        ]

    app_1.dependency_overrides[get_versions] = override_get_versions

    async_client.return_value = AsyncClient(
        transport=ASGITransport(app=app_1), base_url="http://test"
    )

    app_2 = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.credentials_and_registration],
    )

    async with AsyncClient(
        transport=ASGITransport(app=app_2), base_url="http://test"
    ) as client:
        response = await client.post(
            "/ocpi/cpo/2.2.1/credentials/",
            json=CREDENTIALS_TOKEN_CREATE,
            headers=AUTH_HEADERS_A,
        )

    assert response.status_code == 200
    assert response.json()["data"]["token"] == CREDENTIALS_TOKEN_CREATE["token"]
