from pydantic import BaseModel

from ocpi.core.data_types import URL
from ocpi.modules.versions.enums import VersionNumber


class Version(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#121-data
    """

    version: VersionNumber
    url: URL
