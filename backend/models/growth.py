from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class GrowthBase(SQLModel):
    altitude: float = Field(nullable=False)
    average_temperature: float = Field(nullable=False)
    annual_rainfall: float = Field(nullable=False)
    humidity: float = Field(nullable=False)
    soil_ph: float = Field(nullable=False)
    soil_texture: str = Field(nullable=False)
    bean_type_id: str | None =Field(nullable=True, foreign_key="bean_type.id")
    initial_investment: float = Field(nullable=False, default=0)
    available_resources: str | None = Field(nullable=True, max_length=255)

class GrowthFullBase(GrowthBase, BaseEntryModel):
    pass

class Growth(GrowthFullBase, table=True):
    pass
