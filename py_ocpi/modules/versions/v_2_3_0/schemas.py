from pydantic import BaseModel

from py_ocpi.core.data_types import URL
from py_ocpi.core.enums import ModuleID
from py_ocpi.modules.versions.v_2_3_0.enums import InterfaceRole, VersionNumber


class Endpoint(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/version_information_endpoint.asciidoc#122-endpoint-class
    """

    identifier: ModuleID
    role: InterfaceRole
    url: URL


class VersionDetail(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/version_information_endpoint.asciidoc#121-data
    """

    version: VersionNumber
    endpoints: list[Endpoint]
