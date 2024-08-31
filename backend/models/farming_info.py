from datetime import date
from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class FarmingInfoBase(SQLModel):
    watering_date: date = Field(nullable=False)
    plant_health_date: date = Field(nullable=False)
    day_of_planting: date = Field(nullable=False)
    weather_temperature: float = Field(nullable=False)
    soil_moisture: str | None = Field(nullable=True, max_length=50)
    grow_stage: str = Field(nullable=False, max_length=50)
    fertilization_date: date = Field(nullable=False)
    treatment_applied: str | None= Field(nullable=True, max_length=100)
    labor_usage: float = Field(nullable=False)

class FarmingInfoFullBase(FarmingInfoBase, BaseEntryModel):
    pass

class FarmingInfo(FarmingInfoFullBase, table=True):
    pass
