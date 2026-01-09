
from pydantic import BaseModel

from ocpi.core.data_types import (
    URL,
    CiString,
    DateTime,
    DisplayText,
    Number,
    String,
)
from ocpi.modules.locations.schemas import (
    AdditionalGeoLocation,
    EnergyMix,
    GeoLocation,
    Hours,
    StatusSchedule,
)
from ocpi.modules.locations.v_2_3_0.enums import (
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
from ocpi.modules.tokens.v_2_3_0.enums import TokenType


class PublishTokenType(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_locations.asciidoc#mod_locations_publish_token_class
    """

    uid: CiString(max_length=36) | None  # type: ignore
    type: TokenType | None
    visual_number: String(max_length=64) | None  # type: ignore
    issuer: String(max_length=64) | None  # type: ignore
    group_id: CiString(max_length=36) | None  # type: ignore


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_locations.asciidoc#1415-image-class
    """

    url: URL
    thumbnail: URL | None
    category: ImageCategory
    type: CiString(max_length=4)  # type: ignore
    width: int | None
    height: int | None


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
    max_electric_power: int | None
    tariff_ids: list[CiString(max_length=36)] = []  # type: ignore
    terms_and_conditions: URL | None
    last_updated: DateTime


class ConnectorPartialUpdate(BaseModel):
    id: CiString(max_length=36) | None = None  # type: ignore
    standard: ConnectorType | None = None
    format: ConnectorFormat | None = None
    power_type: PowerType | None = None
    max_voltage: int | None = None
    max_amperage: int | None = None
    max_electric_power: int | None = None
    tariff_ids: list[CiString(max_length=36)] | None = None  # type: ignore
    terms_and_conditions: URL | None = None
    last_updated: DateTime | None = None


class EVSEParking(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#evseparking-class
    New in OCPI 2.3.0 - Links an EVSE to a Parking object.
    """

    parking_id: CiString(max_length=36)  # type: ignore
    evse_position: EVSEPosition | None


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#evse-object
    """

    uid: CiString(max_length=36)  # type: ignore
    evse_id: CiString(max_length=48) | None  # type: ignore
    status: Status
    status_schedule: StatusSchedule | None
    capabilities: list[Capability] = []
    connectors: list[Connector]
    floor_level: String(max_length=4) | None  # type: ignore
    coordinates: GeoLocation | None
    physical_reference: String(max_length=16) | None  # type: ignore
    directions: list[DisplayText] = []
    parking_restrictions: list[ParkingRestriction] = []
    # New in OCPI 2.3.0
    parking: list[EVSEParking] = []
    images: list[Image] = []
    # New in OCPI 2.3.0 - NAP-EU compliance field
    accepted_service_providers: list[String(max_length=50)] = []  # type: ignore
    last_updated: DateTime


class EVSEPartialUpdate(BaseModel):
    uid: CiString(max_length=36) | None = None  # type: ignore
    evse_id: CiString(max_length=48) | None = None  # type: ignore
    status: Status | None = None
    status_schedule: StatusSchedule | None = None
    capabilities: list[Capability] | None = None
    connectors: list[Connector] | None = None
    floor_level: String(max_length=4) | None = None  # type: ignore
    coordinates: GeoLocation | None = None
    physical_reference: String(max_length=16) | None = None  # type: ignore
    directions: list[DisplayText] | None = None
    parking_restrictions: list[ParkingRestriction] | None = None
    parking: list[EVSEParking] | None = None
    images: list[Image] | None = None
    accepted_service_providers: list[String(max_length=50)] | None = None  # type: ignore
    last_updated: DateTime | None = None


class Parking(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#parking-object
    New in OCPI 2.3.0 - Describes a parking space for charging.
    Added for EU AFIR compliance (NAP reporting requirements).
    """

    parking_id: CiString(max_length=36)  # type: ignore
    physical_reference: String(max_length=12) | None = None  # type: ignore
    vehicle_types: list[VehicleType]
    max_vehicle_weight: Number | None = None
    max_vehicle_height: Number | None = None
    max_vehicle_length: Number | None = None
    max_vehicle_width: Number | None = None
    parking_space_length: Number | None = None
    parking_space_width: Number | None = None
    dangerous_goods_allowed: bool | None = None
    direction: ParkingDirection | None = None
    drive_through: bool | None = None
    restricted_to_type: bool
    reservation_required: bool
    time_limit: Number | None = None
    roofed: bool | None = None
    images: list[Image] = []
    lighting: bool | None = None
    refrigeration_outlet: bool | None = None
    standards: list[CiString(max_length=36)] = []  # type: ignore
    apds_reference: CiString(max_length=255) | None = None  # type: ignore


class ParkingPartialUpdate(BaseModel):
    """Partial update schema for Parking object."""

    id: CiString(max_length=36) | None = None  # type: ignore
    physical_reference: String(max_length=12) | None = None  # type: ignore
    vehicle_types: list[VehicleType] | None = None
    max_vehicle_weight: Number | None = None
    max_vehicle_height: Number | None = None
    max_vehicle_length: Number | None = None
    max_vehicle_width: Number | None = None
    parking_space_length: Number | None = None
    parking_space_width: Number | None = None
    dangerous_goods_allowed: bool | None = None
    direction: ParkingDirection | None = None
    drive_through: bool | None = None
    restricted_to_type: bool | None = None
    reservation_required: bool | None = None
    time_limit: Number | None = None
    roofed: bool | None = None
    images: list[Image] | None = None
    lighting: bool | None = None
    refrigeration_outlet: bool | None = None
    standards: list[CiString(max_length=36)] | None = None  # type: ignore
    apds_reference: CiString(max_length=255) | None = None  # type: ignore


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.3.0/mod_locations.asciidoc#mod_locations_businessdetails_class
    """

    name: String(max_length=100)  # type: ignore
    website: URL | None
    logo: Image | None


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.3.0-bugfixes/mod_locations.asciidoc#location-object
    """

    country_code: CiString(max_length=2)  # type: ignore
    party_id: CiString(max_length=3)  # type: ignore
    id: CiString(max_length=36)  # type: ignore
    publish: bool
    publish_allowed_to: list[PublishTokenType] = []
    name: String(max_length=255) | None  # type: ignore
    address: String(max_length=45)  # type: ignore
    city: String(max_length=45)  # type: ignore
    postal_code: String(max_length=10) | None  # type: ignore
    state: String(max_length=20) | None  # type: ignore
    country: String(max_length=3)  # type: ignore
    coordinates: GeoLocation
    related_locations: list[AdditionalGeoLocation] = []
    parking_type: ParkingType | None
    evses: list[EVSE] = []
    # New in OCPI 2.3.0 - Parking places for NAP-EU compliance
    parking_places: list[Parking] = []
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
    # New in OCPI 2.3.0 - Help phone for the location
    help_phone: CiString(max_length=25) | None  # type: ignore
    last_updated: DateTime


class LocationPartialUpdate(BaseModel):
    country_code: CiString(max_length=2) | None = None  # type: ignore
    party_id: CiString(max_length=3) | None = None  # type: ignore
    id: CiString(max_length=36) | None = None  # type: ignore
    publish: bool | None = None
    publish_allowed_to: list[PublishTokenType] | None = None
    name: String(max_length=255) | None = None  # type: ignore
    address: String(max_length=45) | None = None  # type: ignore
    city: String(max_length=45) | None = None  # type: ignore
    postal_code: String(max_length=10) | None = None  # type: ignore
    state: String(max_length=20) | None = None  # type: ignore
    country: String(max_length=3) | None = None  # type: ignore
    coordinates: GeoLocation | None = None
    related_locations: list[AdditionalGeoLocation] | None = None
    parking_type: ParkingType | None = None
    evses: list[EVSE] | None = None
    parking_places: list[Parking] | None = None
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
    help_phone: CiString(max_length=25) | None = None  # type: ignore
    last_updated: DateTime | None = None
