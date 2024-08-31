from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class BuyerPreferencesBase(SQLModel):
    roast_level_id: str = Field(nullable=False, foreign_key="roast_level.id")
    origin: str | None = Field(nullable=False, max_length=100)
    processing_method: str = Field(nullable=False, max_length=100)
    flavor_profile: str | None = Field(nullable=True, max_length=100)
    max_price: float = Field(nullable=False, default=9999999)
    min_price: float = Field(nullable=False, default=0)
    stock_quantity: int | None = Field(nullable=True)
    delivery_frequency: str | None = Field(nullable=True, max_length=255)
    favorite_brands: str | None = Field(nullable=True, max_length=255)
    descs: str | None = Field(nullable=True, max_length=255)

class BuyerPreferencesFullBase(BuyerPreferencesBase, BaseEntryModel):
    pass

class BuyerPreferences(BuyerPreferencesFullBase, table=True):
    pass
