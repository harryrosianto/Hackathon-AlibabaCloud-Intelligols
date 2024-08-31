from sqlmodel import Field, Relationship, SQLModel
from typing import TYPE_CHECKING
from models.model import BaseEntryModel
if TYPE_CHECKING:
    from models.user import User
    

class RoleBase(SQLModel):
    name: str = Field(nullable=False, max_length=255)
    descs: str | None = Field(nullable=False, max_length=255)
  
class RoleFullBase(BaseEntryModel, RoleBase):
    pass

class Role(RoleFullBase, table=True):
    users: list["User"] = Relationship(
        back_populates="role", sa_relationship_kwargs={"lazy": "selectin"}
    )

    