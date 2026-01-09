
from pydantic import BaseModel

from py_ocpi.core.data_types import (
    URL,
    CiString,
    DateTime,
    DisplayText,
    Number,
    Price,
    String,
)
from py_ocpi.modules.locations.v_2_2_1.schemas import EnergyMix
from py_ocpi.modules.tariffs.v_2_2_1.enums import (
    DayOfWeek,
    ReservationRestrictionType,
    TariffDimensionType,
    TariffType,
)


class PriceComponent(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#142-pricecomponent-class
    """

    type: TariffDimensionType
    price: Number
    vat: Number | None
    step_size: int


class TariffRestrictions(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#146-tariffrestrictions-class
    """

    start_time: String(5) | None  # type: ignore
    end_time: String(5) | None  # type: ignore
    start_date: String(10) | None  # type: ignore
    end_date: String(10) | None  # type: ignore
    min_kwh: Number | None
    max_kwh: Number | None
    min_current: Number | None
    max_current: Number | None
    min_power: Number | None
    max_power: Number | None
    min_duration: int | None
    max_duration: int | None
    day_of_week: list[DayOfWeek] = []
    reservation: ReservationRestrictionType | None


class TariffElement(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#144-tariffelement-class
    """

    price_components: list[PriceComponent]
    restrictions: TariffRestrictions | None


class Tariff(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#131-tariff-object
    """

    country_code: CiString(2)  # type: ignore
    party_id: CiString(3)  # type: ignore
    id: CiString(36)  # type: ignore
    currency: String(3)  # type: ignore
    type: TariffType | None
    tariff_alt_text: list[DisplayText] = []
    tariff_alt_url: URL | None
    min_price: Price | None
    max_price: Price | None
    elements: list[TariffElement]
    start_date_time: DateTime | None
    end_date_time: DateTime | None
    energy_mix: EnergyMix | None
    last_updated: DateTime
