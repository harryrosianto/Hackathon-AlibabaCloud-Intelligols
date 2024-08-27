from sqlmodel import Field, Relationship, SQLModel
from models.model import BaseEntryModel
from models.user import User

class ProductBase(SQLModel):
    name: str = Field(nullable=False, max_length=255)
    variety: str = Field(nullable=False, max_length=255)
    quality: str = Field(nullable=False, max_length=255)
    price: float = Field(nullable=False, default=0)
    farmer_id: str = Field(foreign_key="user.id", nullable=False)
    descs: str | None= Field(nullable=True, max_length=255)

class ProductFullBase(ProductBase, BaseEntryModel):
    pass

class Product(ProductFullBase, table=True):
    user: "User" = Relationship(back_populates="products",sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Product.farmer_id==User.id",
        })