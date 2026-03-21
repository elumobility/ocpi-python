from unittest.mock import MagicMock

import httpx

from ocpi.core.dependencies import get_versions
from ocpi.core.endpoints import ENDPOINTS
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.v_2_2_1.schemas import VersionDetail

_locations_endpoint = next(
    (
        e
        for e in ENDPOINTS[VersionNumber.v_2_2_1][RoleEnum.cpo]
        if e.identifier == ModuleID.locations
    ),
    None,
)
assert _locations_endpoint is not None, (
    "locations endpoint missing from CPO 2.2.1 ENDPOINTS_LIST"
)

fake_endpoints_data = {
    "data": VersionDetail(
        version=VersionNumber.v_2_2_1,
        endpoints=[_locations_endpoint],
    ).model_dump(),
}

fake_versions_data = {"data": get_versions()}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError(
                f"HTTP {self.status_code}",
                request=MagicMock(),
                response=self,  # type: ignore[arg-type]
            )


# Connector mocks


class MockAsyncClientVersionsAndEndpoints:
    async def get(url, headers=None):
        if url == "versions_url":
            return MockResponse(fake_versions_data, 200)
        else:
            return MockResponse(fake_endpoints_data, 200)

    def build_request(self, request, headers, json):
        return self

    async def send(request):
        return MockResponse(fake_endpoints_data, 200)


class MockAsyncClientGeneratorVersionsAndEndpoints:
    async def __aenter__(self):
        return MockAsyncClientVersionsAndEndpoints

    async def __aexit__(self, *args, **kwargs):
        pass
