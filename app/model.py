from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class APIModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class TravelRequestModel(APIModel):
    destination: str = Field(min_length=1, max_length=120)
    start_date: date
    end_date: date
    base_currency: str = Field(
        default="INR",
        min_length=3,
        max_length=3,
        pattern=r"^[A-Za-z]{3}$",
        description="Three-letter currency code, such as INR or USD.",
    )

    @field_validator("base_currency", mode="before")
    @classmethod
    def normalize_base_currency(cls, value: object) -> object:
        if isinstance(value, str):
            return value.upper()
        return value


class WeatherResponseModel(APIModel):
    date: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")
    condition: str = Field(min_length=1)
    temperature_high: float
    temperature_low: float
    humidity: float = Field(ge=0, le=100)
    rain_chance: float = Field(ge=0, le=100)


class PlaceModel(APIModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    category: str = Field(min_length=1)
    rating: float = Field(ge=0, le=5)
    estimated_time_hours: float = Field(gt=0)
    entry_fee: Optional[float] = Field(default=None, ge=0)


class TravelPlanResponse(APIModel):
    message: str
    weather_data: list[WeatherResponseModel]
    places_data: list[PlaceModel]
    currency_rates: dict[str, float]