
from pydantic import BaseModel

from ocpi.core.data_types import (
    DateTime,
    DisplayText,
    Number,
    String,
)
from ocpi.modules.locations.enums import (
    EnergySourceCategory,
    EnvironmentalImpactCategory,
    Status,
)


class GeoLocation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_geolocation_class
    """

    latitude: String(max_length=10)  # type: ignore
    longitude: String(max_length=11)  # type: ignore


class AdditionalGeoLocation(GeoLocation):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_additionalgeolocation_class
    """

    name: DisplayText | None


class StatusSchedule(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1423-statusschedule-class
    """

    period_begin: DateTime
    period_end: DateTime | None
    status: Status


class RegularHours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1421-regularhours-class
    """

    weekday: int
    period_begin: String(max_length=5)  # type: ignore
    period_end: String(max_length=5)  # type: ignore


class ExceptionalPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1411-exceptionalperiod-class
    """

    period_begin: DateTime
    period_end: DateTime


class Hours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_hours_class
    """

    twentyfourseven: bool
    regular_hours: list[RegularHours] = []
    exceptional_openings: list[ExceptionalPeriod] = []
    exceptional_closings: list[ExceptionalPeriod] = []


class EnergySource(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#147-energysource-class
    """

    source: EnergySourceCategory
    percentage: Number


class EnvironmentalImpact(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#149-environmentalimpact-class
    """

    category: EnvironmentalImpactCategory
    amount: Number


class EnergyMix(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_energymix_class
    """

    is_green_energy: bool
    energy_sources: list[EnergySource]
    environ_impact: EnvironmentalImpact | None
    supplier_name: String(max_length=64)  # type: ignore
    energy_product_name: String(max_length=64)  # type: ignore
