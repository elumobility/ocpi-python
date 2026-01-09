
from pydantic import BaseModel

from py_ocpi.core.data_types import DateTime, Number, String
from py_ocpi.modules.cdrs.v_2_1_1.enums import AuthMethod
from py_ocpi.modules.cdrs.v_2_1_1.schemas import ChargingPeriod
from py_ocpi.modules.locations.v_2_1_1.schemas import Location
from py_ocpi.modules.sessions.v_2_1_1.enums import SessionStatus


class Session(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_sessions.md#31-session-object
    """

    id: String(36)  # type: ignore
    start_datetime: DateTime
    end_datetime: DateTime | None
    kwh: Number
    auth_id: String(36)  # type: ignore
    auth_method: AuthMethod
    location: Location
    meter_id: String(255) | None  # type: ignore
    currency: String(3)  # type: ignore
    charging_periods: list[ChargingPeriod] = []
    total_cost: Number | None
    status: SessionStatus
    last_updated: DateTime


class SessionPartialUpdate(BaseModel):
    id: String(36) | None = None  # type: ignore
    start_datetime: DateTime | None = None
    end_datetime: DateTime | None = None
    kwh: Number | None = None
    auth_id: String(36) | None = None  # type: ignore
    auth_method: AuthMethod | None = None
    location: Location | None = None
    meter_id: String(255) | None = None  # type: ignore
    currency: String(3) | None = None  # type: ignore
    charging_periods: list[ChargingPeriod] | None = None
    total_cost: Number | None = None
    status: SessionStatus | None = None
    last_updated: DateTime | None = None
