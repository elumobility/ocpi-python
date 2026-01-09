
from pydantic import BaseModel

from py_ocpi.core.data_types import DateTime, DisplayText, String
from py_ocpi.modules.tokens.v_2_1_1.enums import (
    Allowed,
    TokenType,
    WhitelistType,
)


class LocationReference(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#42-locationreferences-class
    """

    location_id: String(39)  # type: ignore
    evse_uids: list[String(39)] = []  # type: ignore
    connector_ids: list[String(36)] = []  # type: ignore


class Token(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#32-token-object
    """

    uid: String(36)  # type: ignore
    type: TokenType
    auth_id: String(36)  # type: ignore
    visual_number: String(64) | None  # type: ignore
    issuer: String(64)  # type: ignore
    valid: bool
    whitelist: WhitelistType
    language: String(2) | None  # type: ignore
    last_updated: DateTime


class TokenPartialUpdate(BaseModel):
    uid: String(36) | None = None  # type: ignore
    type: TokenType | None = None
    auth_id: String(36) | None = None  # type: ignore
    visual_number: String(64) | None = None  # type: ignore
    issuer: String(64) | None = None  # type: ignore
    valid: bool | None = None
    whitelist: WhitelistType | None = None
    language: String(2) | None = None  # type: ignore
    last_updated: DateTime | None = None


class AuthorizationInfo(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#31-authorizationinfo-object
    """

    allowed: Allowed
    location: LocationReference | None
    info: DisplayText | None
