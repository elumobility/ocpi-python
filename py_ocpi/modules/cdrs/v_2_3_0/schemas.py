
from pydantic import BaseModel

from py_ocpi.core.data_types import CiString, DateTime, Number, Price, String
from py_ocpi.modules.cdrs.v_2_3_0.enums import AuthMethod, CdrDimensionType
from py_ocpi.modules.locations.v_2_3_0.enums import (
    ConnectorFormat,
    ConnectorType,
    PowerType,
)
from py_ocpi.modules.locations.v_2_3_0.schemas import GeoLocation
from py_ocpi.modules.tariffs.v_2_3_0.schemas import Tariff
from py_ocpi.modules.tokens.v_2_3_0.enums import TokenType


class SignedValue(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_cdrs.asciidoc#148-signedvalue-class
    """

    nature: CiString(32)  # type: ignore
    plain_data: String(512)  # type: ignore
    signed_data: String(5000)  # type: ignore


class SignedData(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_cdrs.asciidoc#147-signeddata-class
    """

    encoding_method: CiString(36)  # type: ignore
    encoding_method_version: int | None
    public_key: String(512) | None  # type: ignore
    signed_values: list[SignedValue]
    url: String(512) | None  # type: ignore


class CdrDimension(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_cdrs.asciidoc#142-cdrdimension-class
    """

    type: CdrDimensionType
    volume: Number


class ChargingPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_cdrs.asciidoc#146-chargingperiod-class
    """

    start_date_time: DateTime
    dimensions: list[CdrDimension]
    tariff_id: CiString(36) | None  # type: ignore


class CdrToken(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_cdrs.asciidoc#145-cdrtoken-class
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    uid: CiString(36)  # type: ignore
    type: TokenType
    contract_id: CiString(36)  # type: ignore


class CdrLocation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_cdrs.asciidoc#144-cdrlocation-class
    """

    id: CiString(36)  # type: ignore
    name: String(255) | None  # type: ignore
    address: String(45)  # type: ignore
    city: String(45)  # type: ignore
    postal_code: String(10) | None  # type: ignore
    state: String(20) | None  # type: ignore
    country: String(3)  # type: ignore
    coordinates: GeoLocation
    evse_id: CiString(48)  # type: ignore
    connector_id: CiString(36)  # type: ignore
    connector_standard: ConnectorType
    connector_format: ConnectorFormat
    connector_power_type: PowerType


class Cdr(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_cdrs.asciidoc#131-cdr-object
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    id: CiString(39)  # type: ignore
    start_date_time: DateTime
    end_date_time: DateTime
    session_id: CiString(36) | None  # type: ignore
    cdr_token: CdrToken
    auth_method: AuthMethod
    authorization_reference: CiString(36) | None  # type: ignore
    cdr_location: CdrLocation
    meter_id: String(255) | None  # type: ignore
    currency: String(3)  # type: ignore
    tariffs: list[Tariff] = []
    charging_periods: list[ChargingPeriod]
    signed_data: SignedData | None
    total_cost: Price
    total_fixed_cost: Price | None
    total_energy: Number
    total_energy_cost: Price | None
    total_time: Number
    total_time_cost: Price | None
    total_parking_time: Number | None
    total_parking_cost: Price | None
    total_reservation_cost: Price | None
    remark: String(255) | None  # type: ignore
    invoice_reference_id: CiString(36) | None  # type: ignore
    credit: bool | None
    credit_reference_id: CiString(39) | None  # type: ignore
    home_charging_compensation: bool | None
    last_updated: DateTime
