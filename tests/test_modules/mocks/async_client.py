from ocpi.core.dependencies import get_versions
from ocpi.core.endpoints import ENDPOINTS
from ocpi.core.enums import ModuleID, RoleEnum
from ocpi.core.data_types import URL
from ocpi.modules.versions.enums import VersionNumber
from ocpi.modules.versions.schemas import Version
from ocpi.modules.versions.v_2_2_1.schemas import VersionDetail as VersionDetail_2_2_1
from ocpi.modules.versions.v_2_3_0.schemas import VersionDetail as VersionDetail_2_3_0

fake_endpoints_data_2_2_1 = {
    "data": VersionDetail_2_2_1(
        version=VersionNumber.v_2_2_1,
        endpoints=[ENDPOINTS[VersionNumber.v_2_2_1][RoleEnum.cpo][ModuleID.locations]],
    ).model_dump(),
}

fake_endpoints_data_2_3_0 = {
    "data": VersionDetail_2_3_0(
        version=VersionNumber.v_2_3_0,
        endpoints=[
            ENDPOINTS[VersionNumber.v_2_3_0][RoleEnum.cpo][ModuleID.locations],
            ENDPOINTS[VersionNumber.v_2_3_0][RoleEnum.emsp][ModuleID.cdrs],
        ],
    ).model_dump(),
}

# Create a versions list that includes both 2.2.1 and 2.3.0
fake_versions_list = [
    Version(
        version=VersionNumber.v_2_2_1,
        url=URL("http://example.com/ocpi/2.2.1/details"),
    ).model_dump(),
    Version(
        version=VersionNumber.v_2_3_0,
        url=URL("http://example.com/ocpi/2.3.0/details"),
    ).model_dump(),
]

fake_versions_data = {"data": fake_versions_list}


class MockResponse:
    def __init__(self, json_data, status_code, headers=None):
        self.json_data = json_data
        self.status_code = status_code
        self.headers = headers or {}

    def json(self):
        return self.json_data


# Connector mocks


class MockAsyncClientVersionsAndEndpoints:
    async def get(self, url, headers=None, **kwargs):
        url_str = str(url)
        # Handle /versions endpoint (returns list of versions)
        if "versions" in url_str and "details" not in url_str:
            return MockResponse(fake_versions_data, 200)
        # Handle /2.3.0/details endpoint (returns VersionDetail with endpoints)
        elif "2.3.0" in url_str and "details" in url_str:
            return MockResponse(fake_endpoints_data_2_3_0, 200)
        # Handle /2.2.1/details endpoint (returns VersionDetail with endpoints)
        elif "2.2.1" in url_str and "details" in url_str:
            return MockResponse(fake_endpoints_data_2_2_1, 200)
        # Default to 2.2.1 for backwards compatibility
        else:
            return MockResponse(fake_endpoints_data_2_2_1, 200)

    def build_request(self, method, url, *, headers=None, json=None, **kwargs):
        # Store method for verification (PATCH vs PUT)
        # httpx.AsyncClient.build_request signature: build_request(method, url, *, headers=None, json=None, ...)
        self.method = method
        self.url = url
        self.json_data = json
        return self

    async def send(self, request):
        # Return success response for both PUT, PATCH, and POST
        # For CDRs (POST), include Location header
        headers = {}
        if self.method == "POST" and "cdrs" in str(self.url):
            headers["Location"] = "http://example.com/ocpi/2.3.0/cdrs/test-cdr-id"
        return MockResponse(
            {"status_code": 1000, "status_message": "Success"}, 200, headers=headers
        )


class MockAsyncClientGeneratorVersionsAndEndpoints:
    async def __aenter__(self):
        return MockAsyncClientVersionsAndEndpoints()

    async def __aexit__(self, *args, **kwargs):
        pass
