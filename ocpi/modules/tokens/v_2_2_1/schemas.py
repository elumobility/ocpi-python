from pydantic import BaseModel

from ocpi.core.data_types import CiString, DateTime, DisplayText, String
from ocpi.modules.sessions.v_2_2_1.enums import ProfileType
from ocpi.modules.tokens.v_2_2_1.enums import (
    AllowedType,
    TokenType,
    WhitelistType,
)


class EnergyContract(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#142-energycontract-class
    """

    supplier_name: String(64)  # type: ignore
    contract_id: String(64) | None  # type: ignore


class LocationReference(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#143-locationreferences-class
    """

    location_id: CiString(36)  # type: ignore
    evse_uids: list[CiString(36)] = []  # type: ignore


class Token(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#132-token-object
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    uid: CiString(36)  # type: ignore
    type: TokenType
    contract_id: CiString(36)  # type: ignore
    visual_number: String(64) | None = None  # type: ignore
    issuer: String(64)  # type: ignore
    group_id: CiString(36) | None = None  # type: ignore
    valid: bool
    whitelist: WhitelistType
    language: String(2) | None = None  # type: ignore
    default_profile_type: ProfileType | None = None
    energy_contract: EnergyContract | None = None
    last_updated: DateTime


class TokenPartialUpdate(BaseModel):
    country_code: CiString(2) | None = None  # type: ignore
    party_id: CiString(3) | None = None  # type: ignore
    uid: CiString(36) | None = None  # type: ignore
    type: TokenType | None = None
    contract_id: CiString(36) | None = None  # type: ignore
    visual_number: String(64) | None = None  # type: ignore
    issuer: String(64) | None = None  # type: ignore
    group_id: CiString(36) | None = None  # type: ignore
    valid: bool | None = None
    whitelist: WhitelistType | None = None
    language: String(2) | None = None  # type: ignore
    default_profile_type: ProfileType | None = None
    energy_contract: EnergyContract | None = None
    last_updated: DateTime | None = None


class AuthorizationInfo(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#131-authorizationinfo-object
    """

    allowed: AllowedType
    token: Token
    location: LocationReference | None
    authorization_reference: CiString(36) | None  # type: ignore
    info: DisplayText | None
