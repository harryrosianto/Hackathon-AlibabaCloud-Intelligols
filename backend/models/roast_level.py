from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class RoastLevelBase(SQLModel):
    name: str = Field(nullable=False, max_length=50)
    descs: str | None = Field(nullable=True, max_length=255)

class RoastLevelFullBase(RoastLevelBase, BaseEntryModel):
    pass

class RoastLevel(RoastLevelFullBase, table=True):
    pass
