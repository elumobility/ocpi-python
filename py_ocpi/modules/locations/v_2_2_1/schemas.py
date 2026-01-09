from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.modules.tokens.v_2_2_1.enums import TokenType
from py_ocpi.modules.locations.v_2_2_1.enums import (
    ParkingType,
    ParkingRestriction,
    Facility,
    Status,
    Capability,
    ConnectorFormat,
    ConnectorType,
    PowerType,
    ImageCategory,
)
from py_ocpi.modules.locations.schemas import (
    AdditionalGeoLocation,
    EnergyMix,
    GeoLocation,
    Hours,
    StatusSchedule,
)
from py_ocpi.core.data_types import (
    URL,
    CiString,
    DisplayText,
    String,
    DateTime,
)


class PublishTokenType(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_publish_token_class
    """

    uid: Optional[CiString(max_length=36)]  # type: ignore
    type: Optional[TokenType]
    visual_number: Optional[String(max_length=64)]  # type: ignore
    issuer: Optional[String(max_length=64)]  # type: ignore
    group_id: Optional[CiString(max_length=36)]  # type: ignore


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1415-image-class
    """

    url: URL
    thumbnail: Optional[URL]
    category: ImageCategory
    type: CiString(max_length=4)  # type: ignore
    width: Optional[int]
    height: Optional[int]


class Connector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#133-connector-object
    """

    id: CiString(max_length=36)  # type: ignore
    standard: ConnectorType
    format: ConnectorFormat
    power_type: PowerType
    max_voltage: int
    max_amperage: int
    max_electric_power: Optional[int]
    tariff_ids: List[CiString(max_length=36)] = []  # type: ignore
    terms_and_conditions: Optional[URL]
    last_updated: DateTime


class ConnectorPartialUpdate(BaseModel):
    id: Optional[CiString(max_length=36)] = None  # type: ignore
    standard: Optional[ConnectorType] = None
    format: Optional[ConnectorFormat] = None
    power_type: Optional[PowerType] = None
    max_voltage: Optional[int] = None
    max_amperage: Optional[int] = None
    max_electric_power: Optional[Optional[int]] = None
    tariff_ids: Optional[List[CiString(max_length=36)]] = None  # type: ignore
    terms_and_conditions: Optional[URL] = None
    last_updated: Optional[DateTime] = None


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_evse_object
    """

    uid: CiString(max_length=36)  # type: ignore
    evse_id: Optional[CiString(max_length=48)]  # type: ignore
    status: Status
    status_schedule: Optional[StatusSchedule]
    capabilities: List[Capability] = []
    connectors: List[Connector]
    floor_level: Optional[String(max_length=4)]  # type: ignore
    coordinates: Optional[GeoLocation]
    physical_reference: Optional[String(max_length=16)]  # type: ignore
    directions: List[DisplayText] = []
    parking_restrictions: List[ParkingRestriction] = []
    images: List[Image] = []
    last_updated: DateTime


class EVSEPartialUpdate(BaseModel):
    uid: Optional[CiString(max_length=36)] = None  # type: ignore
    evse_id: Optional[CiString(max_length=48)] = None  # type: ignore
    status: Optional[Status] = None
    status_schedule: Optional[StatusSchedule] = None
    capabilities: Optional[List[Capability]] = None
    connectors: Optional[List[Connector]] = None
    floor_level: Optional[String(max_length=4)] = None  # type: ignore
    coordinates: Optional[GeoLocation] = None
    physical_reference: Optional[String(max_length=16)] = None  # type: ignore
    directions: Optional[List[DisplayText]] = None
    parking_restrictions: Optional[List[ParkingRestriction]] = None
    images: Optional[List[Image]] = None
    last_updated: Optional[DateTime] = None


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_businessdetails_class
    """

    name: String(max_length=100)  # type: ignore
    website: Optional[URL]
    logo: Optional[Image]


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#131-location-object
    """

    country_code: CiString(max_length=2)  # type: ignore
    party_id: CiString(max_length=3)  # type: ignore
    id: CiString(max_length=36)  # type: ignore
    publish: bool
    publish_allowed_to: List[PublishTokenType] = []
    name: Optional[String(max_length=255)]  # type: ignore
    address: String(max_length=45)  # type: ignore
    city: String(max_length=45)  # type: ignore
    postal_code: Optional[String(max_length=10)]  # type: ignore
    state: Optional[String(max_length=20)]  # type: ignore
    country: String(max_length=3)  # type: ignore
    coordinates: GeoLocation
    related_locations: List[AdditionalGeoLocation] = []
    parking_type: Optional[ParkingType]
    evses: List[EVSE] = []
    directions: List[DisplayText] = []
    operator: Optional[BusinessDetails]
    suboperator: Optional[BusinessDetails]
    owner: Optional[BusinessDetails]
    facilities: List[Facility] = []
    time_zone: String(max_length=255)  # type: ignore
    opening_times: Optional[Hours]
    charging_when_closed: Optional[bool]
    images: List[Image] = []
    energy_mix: Optional[EnergyMix]
    last_updated: DateTime


class LocationPartialUpdate(BaseModel):
    country_code: Optional[CiString(max_length=2)] = None  # type: ignore
    party_id: Optional[CiString(max_length=3)] = None  # type: ignore
    id: Optional[CiString(max_length=36)] = None  # type: ignore
    publish: Optional[bool] = None
    publish_allowed_to: Optional[List[PublishTokenType]] = None
    name: Optional[String(max_length=255)] = None  # type: ignore
    address: Optional[String(max_length=45)] = None  # type: ignore
    city: Optional[String(max_length=45)] = None  # type: ignore
    postal_code: Optional[String(max_length=10)] = None  # type: ignore
    state: Optional[String(max_length=20)] = None  # type: ignore
    country: Optional[String(max_length=3)] = None  # type: ignore
    coordinates: Optional[GeoLocation] = None
    related_locations: Optional[List[AdditionalGeoLocation]] = None
    parking_type: Optional[ParkingType] = None
    evses: Optional[List[EVSE]] = None
    directions: Optional[List[DisplayText]] = None
    operator: Optional[BusinessDetails] = None
    suboperator: Optional[BusinessDetails] = None
    owner: Optional[BusinessDetails] = None
    facilities: Optional[List[Facility]] = None
    time_zone: Optional[String(max_length=255)] = None  # type: ignore
    opening_times: Optional[Hours] = None
    charging_when_closed: Optional[bool] = None
    images: Optional[List[Image]] = None
    energy_mix: Optional[EnergyMix] = None
    last_updated: Optional[DateTime] = None
