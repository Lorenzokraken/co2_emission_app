from pydantic import BaseModel
from typing import List, Optional

class CountryBase(BaseModel):
    country_id: int
    name: str
    iso_code: Optional[str] = None
    surface_km2: Optional[int] = None

    class Config:
        from_attributes = True

class YearBase(BaseModel):
    year_id: int
    year: int

    class Config:
        from_attributes = True

class EmissionBase(BaseModel):
    emission_id: int
    country_id: int
    year_id: int
    co2: Optional[float] = None
    co2_per_km2: Optional[float] = None
    population: Optional[int] = None

    class Config:
        from_attributes = True

class ChartData(BaseModel):
    countries: List[str]
    years: List[int]
    series: List[dict]

class ChartRequest(BaseModel):
    country_ids: List[int]
    year_start: int
    year_end: int
    ai: bool = False
    show_density: bool = False