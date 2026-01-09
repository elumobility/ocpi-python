from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.modules.cdrs.v_2_3_0.enums import AuthMethod
from py_ocpi.modules.cdrs.v_2_3_0.schemas import CdrToken, ChargingPeriod
from py_ocpi.modules.sessions.v_2_3_0.enums import ProfileType, SessionStatus
from py_ocpi.core.data_types import CiString, Number, Price, String, DateTime


class Session(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_sessions.asciidoc#131-session-object
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    id: CiString(36)  # type: ignore
    start_date_time: DateTime
    end_date_time: Optional[DateTime]
    kwh: Number
    cdr_token: CdrToken
    auth_method: AuthMethod
    authorization_reference: Optional[CiString(36)]  # type: ignore
    location_id: CiString(36)  # type: ignore
    evse_uid: CiString(36)  # type: ignore
    connector_id: CiString(36)  # type: ignore
    meter_id: Optional[String(255)]  # type: ignore
    currency: String(3)  # type: ignore
    charging_periods: List[ChargingPeriod] = []
    total_cost: Optional[Price]
    status: SessionStatus
    last_updated: DateTime


class SessionPartialUpdate(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_sessions.asciidoc#131-session-object
    """

    country_code: Optional[CiString(2)] = None  # type: ignore
    party_id: Optional[CiString(3)] = None  # type: ignore
    id: Optional[CiString(36)] = None  # type: ignore
    start_date_time: Optional[DateTime] = None
    end_date_time: Optional[DateTime] = None
    kwh: Optional[Number] = None
    cdr_token: Optional[CdrToken] = None
    auth_method: Optional[AuthMethod] = None
    authorization_reference: Optional[CiString(36)] = None  # type: ignore
    location_id: Optional[CiString(36)] = None  # type: ignore
    evse_uid: Optional[CiString(36)] = None  # type: ignore
    connector_id: Optional[CiString(36)] = None  # type: ignore
    meter_id: Optional[String(255)] = None  # type: ignore
    currency: Optional[String(3)] = None  # type: ignore
    charging_periods: Optional[List[ChargingPeriod]] = None
    total_cost: Optional[Price] = None
    status: Optional[SessionStatus] = None
    last_updated: Optional[DateTime] = None


class ChargingPreferences(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_sessions.asciidoc#132-chargingpreferences-object
    """

    profile_type: ProfileType
    departure_time: Optional[DateTime] = None
    energy_need: Optional[Number] = None
    discharge_allowed: Optional[bool] = None
