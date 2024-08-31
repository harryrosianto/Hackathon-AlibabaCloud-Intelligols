from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class MarketplaceBase(SQLModel):
    name: str = Field(nullable=False, max_length=50)
    origin: str | None = Field(nullable=None, max_length=100)
    processing_method: str = Field(nullable=False, max_length=100)
    bean_type_id: str =Field(nullable=False, foreign_key="bean_type.id")
    roast_level_id: str = Field(nullable=False, foreign_key="roast_level.id")
    price: float = Field(nullable=False, default=0)
    stock_quantity: int = Field(nullable=False, default=0)
    image: str | None = Field(nullable=True, max_length=255)

class MarketplaceFullBase(MarketplaceBase, BaseEntryModel):
    pass

class Marketplace(MarketplaceFullBase, table=True):
    pass
