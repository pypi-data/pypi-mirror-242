from enum import StrEnum, IntEnum
from typing import TypedDict, Optional


class FuelType(IntEnum):
    SuperUnleaded = 1
    Unleaded = 2
    PremiumDiesel = 4
    Diesel = 5


class SortMethod(StrEnum):
    Closest = "distance"
    Cheapest = "price"


class Geometry(TypedDict):
    type: str
    coordinates: list[float]


class ReviewEntry(TypedDict):
    count: int
    avg_rating: float


class EntryProperties(TypedDict):
    price: float
    fuel_type: FuelType
    user_id: Optional[int]
    recorded_time: Optional[str]
    user_name: Optional[str]
    idstation: int
    fuel_brand: str
    fuel_brand_name: str
    name: str
    address1: str
    address2: str
    town: str
    county: str
    postcode: str
    distance_in_miles_from_given_coords: float
    reviews: ReviewEntry


class SearchEntry(TypedDict):
    geometry: Geometry
    properties: EntryProperties


class SearchEntriesCollection(TypedDict):
    data: list[SearchEntry]
