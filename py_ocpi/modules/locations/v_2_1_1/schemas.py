from typing import List, Optional

from pydantic import BaseModel

from py_ocpi.core.data_types import DisplayText, DateTime, String, URL

from py_ocpi.modules.locations.schemas import (
    AdditionalGeoLocation,
    EnergyMix,
    GeoLocation,
    Hours,
    StatusSchedule,
)
from py_ocpi.modules.locations.v_2_1_1.enums import (
    Capability,
    ConnectorFormat,
    ConnectorType,
    Facility,
    LocationType,
    ParkingRestriction,
    PowerType,
    ImageCategory,
    Status,
)


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#414-image-class
    """

    url: URL
    thumbnail: Optional[URL]
    category: ImageCategory
    type: String(max_length=4)  # type: ignore
    width: Optional[int]
    height: Optional[int]


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#41-businessdetails-class
    """

    name: String(max_length=100)  # type: ignore
    website: Optional[URL]
    logo: Optional[Image]


class Connector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#33-connector-object
    """

    id: String(max_length=36)  # type: ignore
    standard: ConnectorType
    format: ConnectorFormat
    power_type: PowerType
    voltage: int
    amperage: int
    tariff_id: String(max_length=36)  # type: ignore
    terms_and_conditions: Optional[URL]
    last_updated: DateTime


class ConnectorPartialUpdate(BaseModel):
    id: Optional[String(max_length=36)] = None  # type: ignore
    standard: Optional[ConnectorType] = None
    format: Optional[ConnectorFormat] = None
    power_type: Optional[PowerType] = None
    voltage: Optional[int] = None
    amperage: Optional[int] = None
    tariff_id: Optional[String(max_length=36)] = None  # type: ignore
    terms_and_conditions: Optional[URL] = None
    last_updated: Optional[DateTime] = None


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#32-evse-object
    """

    uid: String(max_length=39)  # type: ignore
    evse_id: Optional[String(max_length=48)]  # type: ignore
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
    uid: Optional[String(max_length=39)] = None  # type: ignore
    evse_id: Optional[String(max_length=48)] = None  # type: ignore
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


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#31-location-object
    """

    id: String(max_length=39)  # type: ignore
    type: LocationType
    name: Optional[String(max_length=255)]  # type: ignore
    address: String(max_length=45)  # type: ignore
    city: String(max_length=45)  # type: ignore
    postal_code: Optional[String(max_length=10)]  # type: ignore
    country: String(max_length=3)  # type: ignore
    coordinates: GeoLocation
    related_locations: List[AdditionalGeoLocation] = []
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
    id: Optional[String(max_length=39)] = None  # type: ignore
    type: Optional[LocationType] = None
    name: Optional[String(max_length=255)] = None  # type: ignore
    address: Optional[String(max_length=45)] = None  # type: ignore
    city: Optional[String(max_length=45)] = None  # type: ignore
    postal_code: Optional[String(max_length=10)] = None  # type: ignore
    country: Optional[String(max_length=3)] = None  # type: ignore
    coordinates: Optional[GeoLocation] = None
    related_locations: Optional[List[AdditionalGeoLocation]] = None
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
