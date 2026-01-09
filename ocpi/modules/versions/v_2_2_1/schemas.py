from pydantic import BaseModel

from ocpi.core.data_types import URL
from ocpi.core.enums import ModuleID
from ocpi.modules.versions.v_2_2_1.enums import InterfaceRole, VersionNumber


class Endpoint(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#122-endpoint-class
    """

    identifier: ModuleID
    role: InterfaceRole
    url: URL


class VersionDetail(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#121-data
    """

    version: VersionNumber
    endpoints: list[Endpoint]
