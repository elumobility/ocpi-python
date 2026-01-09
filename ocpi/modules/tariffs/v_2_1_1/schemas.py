from pydantic import BaseModel

from ocpi.core.data_types import URL, DateTime, DisplayText, Number, String
from ocpi.modules.locations.v_2_1_1.schemas import EnergyMix
from ocpi.modules.tariffs.v_2_1_1.enums import (
    DayOfWeek,
    TariffDimensionType,
)


class PriceComponent(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#42-pricecomponent-class
    """

    type: TariffDimensionType
    price: Number
    step_size: int


class TariffRestrictions(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#45-tariffrestrictions-class
    """

    start_time: String(5) | None  # type: ignore
    end_time: String(5) | None  # type: ignore
    start_date: String(10) | None  # type: ignore
    end_date: String(10) | None  # type: ignore
    min_kwh: Number | None
    max_kwh: Number | None
    min_power: Number | None
    max_power: Number | None
    min_duration: int | None
    max_duration: int | None
    day_of_week: list[DayOfWeek] = []


class TariffElement(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#43-tariffelement-class
    """

    price_components: list[PriceComponent]
    restrictions: TariffRestrictions | None


class Tariff(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#31-tariff-object
    """

    id: String(36)  # type: ignore
    currency: String(3)  # type: ignore
    tariff_alt_text: list[DisplayText] = []
    tariff_alt_url: URL | None
    elements: list[TariffElement]
    energy_mix: EnergyMix | None
    last_updated: DateTime


class TariffPartialUpdate(BaseModel):
    id: String(36) | None = None  # type: ignore
    currency: String(3) | None = None  # type: ignore
    tariff_alt_text: list[DisplayText] | None = None
    tariff_alt_url: URL | None = None
    elements: list[TariffElement] | None = None
    energy_mix: EnergyMix | None = None
    last_updated: DateTime | None = None
