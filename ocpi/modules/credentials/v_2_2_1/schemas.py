from pydantic import BaseModel

from ocpi.core.data_types import URL, CiString, String
from ocpi.core.enums import RoleEnum
from ocpi.modules.locations.v_2_2_1.schemas import BusinessDetails


class CredentialsRole(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#141-credentialsrole-class
    """

    role: RoleEnum
    business_details: BusinessDetails
    party_id: CiString(3)  # type: ignore
    country_code: CiString(2)  # type: ignore


class Credentials(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#131-credentials-object
    """

    token: String(64)  # type: ignore
    url: URL
    roles: list[CredentialsRole]
