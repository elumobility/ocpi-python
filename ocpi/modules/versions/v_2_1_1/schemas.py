from pydantic import BaseModel

from ocpi.core.data_types import URL
from ocpi.core.enums import ModuleID
from ocpi.modules.versions.v_2_1_1.enums import VersionNumber


class Endpoint(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/version_information_endpoint.md#endpoint-class
    """

    identifier: ModuleID
    url: URL


class VersionDetail(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/version_information_endpoint.md#data-1
    """

    version: VersionNumber
    endpoints: list[Endpoint]
