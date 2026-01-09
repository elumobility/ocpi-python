from typing import List, Optional

from pydantic import BaseModel

from py_ocpi.core.data_types import (
    URL,
    CiString,
    DateTime,
    DisplayText,
    Number,
    String,
)
from py_ocpi.modules.locations.schemas import (
    AdditionalGeoLocation,
    EnergyMix,
    GeoLocation,
    Hours,
    StatusSchedule,
)
from py_ocpi.modules.locations.v_2_3_0.enums import (
    Capability,
    ConnectorFormat,
    ConnectorType,
    EVSEPosition,
    Facility,
    ImageCategory,
    ParkingDirection,
    ParkingRestriction,
    ParkingType,
    PowerType,
    Status,
    VehicleType,
)
from py_ocpi.modules.tokens.v_2_3_0.enums import TokenType


class PublishTokenType(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_locations.asciidoc#mod_locations_publish_token_class
    """

    uid: Optional[CiString(max_length=36)]  # type: ignore
    type: Optional[TokenType]
    visual_number: Optional[String(max_length=64)]  # type: ignore
    issuer: Optional[String(max_length=64)]  # type: ignore
    group_id: Optional[CiString(max_length=36)]  # type: ignore


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_locations.asciidoc#1415-image-class
    """

    url: URL
    thumbnail: Optional[URL]
    category: ImageCategory
    type: CiString(max_length=4)  # type: ignore
    width: Optional[int]
    height: Optional[int]


class Connector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#connector-object
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
    id: Optional[CiString(max_length=36)]  # type: ignore
    standard: Optional[ConnectorType]
    format: Optional[ConnectorFormat]
    power_type: Optional[PowerType]
    max_voltage: Optional[int]
    max_amperage: Optional[int]
    max_electric_power: Optional[Optional[int]]
    tariff_ids: Optional[List[CiString(max_length=36)]]  # type: ignore
    terms_and_conditions: Optional[URL]
    last_updated: Optional[DateTime]


class EVSEParking(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#evseparking-class
    New in OCPI 2.3.0 - Links an EVSE to a Parking object.
    """

    parking_id: CiString(max_length=36)  # type: ignore
    evse_position: Optional[EVSEPosition]


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#evse-object
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
    # New in OCPI 2.3.0
    parking: List[EVSEParking] = []
    images: List[Image] = []
    # New in OCPI 2.3.0 - NAP-EU compliance field
    accepted_service_providers: List[String(max_length=50)] = []  # type: ignore
    last_updated: DateTime


class EVSEPartialUpdate(BaseModel):
    uid: Optional[CiString(max_length=36)]  # type: ignore
    evse_id: Optional[CiString(max_length=48)]  # type: ignore
    status: Optional[Status]
    status_schedule: Optional[StatusSchedule]
    capabilities: Optional[List[Capability]]
    connectors: Optional[List[Connector]]
    floor_level: Optional[String(max_length=4)]  # type: ignore
    coordinates: Optional[GeoLocation]
    physical_reference: Optional[String(max_length=16)]  # type: ignore
    directions: Optional[List[DisplayText]]
    parking_restrictions: Optional[List[ParkingRestriction]]
    parking: Optional[List[EVSEParking]]
    images: Optional[List[Image]]
    accepted_service_providers: Optional[List[String(max_length=50)]]  # type: ignore
    last_updated: Optional[DateTime]


class Parking(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#parking-object
    New in OCPI 2.3.0 - Describes a parking space for charging.
    Added for EU AFIR compliance (NAP reporting requirements).
    """

    id: CiString(max_length=36)  # type: ignore
    physical_reference: Optional[String(max_length=12)]  # type: ignore
    vehicle_types: List[VehicleType]
    max_vehicle_weight: Optional[Number]
    max_vehicle_height: Optional[Number]
    max_vehicle_length: Optional[Number]
    max_vehicle_width: Optional[Number]
    parking_space_length: Optional[Number]
    parking_space_width: Optional[Number]
    dangerous_goods_allowed: Optional[bool]
    direction: Optional[ParkingDirection]
    drive_through: Optional[bool]
    restricted_to_type: bool
    reservation_required: bool
    time_limit: Optional[Number]
    roofed: Optional[bool]
    images: List[Image] = []
    lighting: Optional[bool]
    refrigeration_outlet: Optional[bool]
    standards: List[CiString(max_length=36)] = []  # type: ignore
    apds_reference: Optional[CiString(max_length=255)]  # type: ignore


class ParkingPartialUpdate(BaseModel):
    """Partial update schema for Parking object."""

    id: Optional[CiString(max_length=36)]  # type: ignore
    physical_reference: Optional[String(max_length=12)]  # type: ignore
    vehicle_types: Optional[List[VehicleType]]
    max_vehicle_weight: Optional[Number]
    max_vehicle_height: Optional[Number]
    max_vehicle_length: Optional[Number]
    max_vehicle_width: Optional[Number]
    parking_space_length: Optional[Number]
    parking_space_width: Optional[Number]
    dangerous_goods_allowed: Optional[bool]
    direction: Optional[ParkingDirection]
    drive_through: Optional[bool]
    restricted_to_type: Optional[bool]
    reservation_required: Optional[bool]
    time_limit: Optional[Number]
    roofed: Optional[bool]
    images: Optional[List[Image]]
    lighting: Optional[bool]
    refrigeration_outlet: Optional[bool]
    standards: Optional[List[CiString(max_length=36)]]  # type: ignore
    apds_reference: Optional[CiString(max_length=255)]  # type: ignore


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_locations.asciidoc#mod_locations_businessdetails_class
    """

    name: String(max_length=100)  # type: ignore
    website: Optional[URL]
    logo: Optional[Image]


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#location-object
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
    # New in OCPI 2.3.0 - Parking places for NAP-EU compliance
    parking_places: List[Parking] = []
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
    # New in OCPI 2.3.0 - Help phone for the location
    help_phone: Optional[CiString(max_length=25)]  # type: ignore
    last_updated: DateTime


class LocationPartialUpdate(BaseModel):
    country_code: Optional[CiString(max_length=2)]  # type: ignore
    party_id: Optional[CiString(max_length=3)]  # type: ignore
    id: Optional[CiString(max_length=36)]  # type: ignore
    publish: Optional[bool]
    publish_allowed_to: Optional[List[PublishTokenType]]
    name: Optional[String(max_length=255)]  # type: ignore
    address: Optional[String(max_length=45)]  # type: ignore
    city: Optional[String(max_length=45)]  # type: ignore
    postal_code: Optional[String(max_length=10)]  # type: ignore
    state: Optional[String(max_length=20)]  # type: ignore
    country: Optional[String(max_length=3)]  # type: ignore
    coordinates: Optional[GeoLocation]
    related_locations: Optional[List[AdditionalGeoLocation]]
    parking_type: Optional[ParkingType]
    evses: Optional[List[EVSE]]
    parking_places: Optional[List[Parking]]
    directions: Optional[List[DisplayText]]
    operator: Optional[BusinessDetails]
    suboperator: Optional[BusinessDetails]
    owner: Optional[BusinessDetails]
    facilities: Optional[List[Facility]]
    time_zone: Optional[String(max_length=255)]  # type: ignore
    opening_times: Optional[Hours]
    charging_when_closed: Optional[bool]
    images: Optional[List[Image]]
    energy_mix: Optional[EnergyMix]
    help_phone: Optional[CiString(max_length=25)]  # type: ignore
    last_updated: Optional[DateTime]
