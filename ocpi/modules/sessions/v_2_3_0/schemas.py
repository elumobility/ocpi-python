from pydantic import BaseModel

from ocpi.core.data_types import CiString, DateTime, Number, Price, String
from ocpi.modules.cdrs.v_2_3_0.enums import AuthMethod
from ocpi.modules.cdrs.v_2_3_0.schemas import CdrToken, ChargingPeriod
from ocpi.modules.sessions.v_2_3_0.enums import ProfileType, SessionStatus


class Session(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_sessions.asciidoc#131-session-object
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    id: CiString(36)  # type: ignore
    start_date_time: DateTime
    end_date_time: DateTime | None
    kwh: Number
    cdr_token: CdrToken
    auth_method: AuthMethod
    authorization_reference: CiString(36) | None  # type: ignore
    location_id: CiString(36)  # type: ignore
    evse_uid: CiString(36)  # type: ignore
    connector_id: CiString(36)  # type: ignore
    meter_id: String(255) | None  # type: ignore
    currency: String(3)  # type: ignore
    charging_periods: list[ChargingPeriod] = []
    total_cost: Price | None
    status: SessionStatus
    last_updated: DateTime


class SessionPartialUpdate(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_sessions.asciidoc#131-session-object
    """

    country_code: CiString(2) | None = None  # type: ignore
    party_id: CiString(3) | None = None  # type: ignore
    id: CiString(36) | None = None  # type: ignore
    start_date_time: DateTime | None = None
    end_date_time: DateTime | None = None
    kwh: Number | None = None
    cdr_token: CdrToken | None = None
    auth_method: AuthMethod | None = None
    authorization_reference: CiString(36) | None = None  # type: ignore
    location_id: CiString(36) | None = None  # type: ignore
    evse_uid: CiString(36) | None = None  # type: ignore
    connector_id: CiString(36) | None = None  # type: ignore
    meter_id: String(255) | None = None  # type: ignore
    currency: String(3) | None = None  # type: ignore
    charging_periods: list[ChargingPeriod] | None = None
    total_cost: Price | None = None
    status: SessionStatus | None = None
    last_updated: DateTime | None = None


class ChargingPreferences(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_sessions.asciidoc#132-chargingpreferences-object
    """

    profile_type: ProfileType
    departure_time: DateTime | None = None
    energy_need: Number | None = None
    discharge_allowed: bool | None = None
