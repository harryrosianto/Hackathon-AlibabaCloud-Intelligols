from pydantic import Field
from sqlmodel import Relationship, SQLModel

from models.base import BaseEntryModel

from .user import User


class ProductBase(SQLModel):
    name: str = Field(nullable=False, max_length=255)
    variety: str = Field(nullable=False, max_length=255)
    quality: str  = Field(nullable=False, max_length=255)
    price: float  = Field(nullable=False, default=0)
    farmer_id: str = Field(nullable=False, foreign_key="user.id")
    description: str | None = Field(nullable= True, max_length=255)

class ProductFullBase(ProductBase, BaseEntryModel):
    pass

class Product(ProductFullBase, table=True):
    user: User = Relationship(back_populates="products", sa_relationship={'lazy': 'selectin'})