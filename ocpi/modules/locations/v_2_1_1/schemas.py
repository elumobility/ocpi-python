
from pydantic import BaseModel

from ocpi.core.data_types import URL, DateTime, DisplayText, String
from ocpi.modules.locations.schemas import (
    AdditionalGeoLocation,
    EnergyMix,
    GeoLocation,
    Hours,
    StatusSchedule,
)
from ocpi.modules.locations.v_2_1_1.enums import (
    Capability,
    ConnectorFormat,
    ConnectorType,
    Facility,
    ImageCategory,
    LocationType,
    ParkingRestriction,
    PowerType,
    Status,
)


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#414-image-class
    """

    url: URL
    thumbnail: URL | None
    category: ImageCategory
    type: String(max_length=4)  # type: ignore
    width: int | None
    height: int | None


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#41-businessdetails-class
    """

    name: String(max_length=100)  # type: ignore
    website: URL | None
    logo: Image | None


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
    terms_and_conditions: URL | None
    last_updated: DateTime


class ConnectorPartialUpdate(BaseModel):
    id: String(max_length=36) | None = None  # type: ignore
    standard: ConnectorType | None = None
    format: ConnectorFormat | None = None
    power_type: PowerType | None = None
    voltage: int | None = None
    amperage: int | None = None
    tariff_id: String(max_length=36) | None = None  # type: ignore
    terms_and_conditions: URL | None = None
    last_updated: DateTime | None = None


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#32-evse-object
    """

    uid: String(max_length=39)  # type: ignore
    evse_id: String(max_length=48) | None  # type: ignore
    status: Status
    status_schedule: StatusSchedule | None
    capabilities: list[Capability] = []
    connectors: list[Connector]
    floor_level: String(max_length=4) | None  # type: ignore
    coordinates: GeoLocation | None
    physical_reference: String(max_length=16) | None  # type: ignore
    directions: list[DisplayText] = []
    parking_restrictions: list[ParkingRestriction] = []
    images: list[Image] = []
    last_updated: DateTime


class EVSEPartialUpdate(BaseModel):
    uid: String(max_length=39) | None = None  # type: ignore
    evse_id: String(max_length=48) | None = None  # type: ignore
    status: Status | None = None
    status_schedule: StatusSchedule | None = None
    capabilities: list[Capability] | None = None
    connectors: list[Connector] | None = None
    floor_level: String(max_length=4) | None = None  # type: ignore
    coordinates: GeoLocation | None = None
    physical_reference: String(max_length=16) | None = None  # type: ignore
    directions: list[DisplayText] | None = None
    parking_restrictions: list[ParkingRestriction] | None = None
    images: list[Image] | None = None
    last_updated: DateTime | None = None


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#31-location-object
    """

    id: String(max_length=39)  # type: ignore
    type: LocationType
    name: String(max_length=255) | None  # type: ignore
    address: String(max_length=45)  # type: ignore
    city: String(max_length=45)  # type: ignore
    postal_code: String(max_length=10) | None  # type: ignore
    country: String(max_length=3)  # type: ignore
    coordinates: GeoLocation
    related_locations: list[AdditionalGeoLocation] = []
    evses: list[EVSE] = []
    directions: list[DisplayText] = []
    operator: BusinessDetails | None
    suboperator: BusinessDetails | None
    owner: BusinessDetails | None
    facilities: list[Facility] = []
    time_zone: String(max_length=255)  # type: ignore
    opening_times: Hours | None
    charging_when_closed: bool | None
    images: list[Image] = []
    energy_mix: EnergyMix | None
    last_updated: DateTime


class LocationPartialUpdate(BaseModel):
    id: String(max_length=39) | None = None  # type: ignore
    type: LocationType | None = None
    name: String(max_length=255) | None = None  # type: ignore
    address: String(max_length=45) | None = None  # type: ignore
    city: String(max_length=45) | None = None  # type: ignore
    postal_code: String(max_length=10) | None = None  # type: ignore
    country: String(max_length=3) | None = None  # type: ignore
    coordinates: GeoLocation | None = None
    related_locations: list[AdditionalGeoLocation] | None = None
    evses: list[EVSE] | None = None
    directions: list[DisplayText] | None = None
    operator: BusinessDetails | None = None
    suboperator: BusinessDetails | None = None
    owner: BusinessDetails | None = None
    facilities: list[Facility] | None = None
    time_zone: String(max_length=255) | None = None  # type: ignore
    opening_times: Hours | None = None
    charging_when_closed: bool | None = None
    images: list[Image] | None = None
    energy_mix: EnergyMix | None = None
    last_updated: DateTime | None = None
