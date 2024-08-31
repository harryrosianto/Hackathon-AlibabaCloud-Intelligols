from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class BeanTypeBase(SQLModel):
    name: str = Field(nullable=False, max_length=50)
    descs: str | None = Field(nullable=True, max_length=255)

class BeanTypeFullBase(BeanTypeBase, BaseEntryModel):
    pass

class BeanType(BeanTypeFullBase, table=True):
    pass
