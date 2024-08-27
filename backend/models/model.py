from datetime import datetime, timezone
from sqlmodel import SQLModel as _SQLModel, Field
from sqlalchemy.orm import declared_attr
from stringcase import snakecase
import ulid
from sqlalchemy import Column
from sqlalchemy.sql import func

class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

def generate_ulid() -> str:
    return str(ulid.ulid())

class BaseFieldModel(SQLModel):
    id: str | None = Field(
        default_factory=generate_ulid, 
        primary_key=True, 
        index=True, 
        nullable=False, 
        max_length=26
    )

class BaseEntryModel(BaseFieldModel):
    created_by: str = Field(default="admin")
    updated_by: str = Field(default="admin")
    updated_at: datetime | None = Field(
        default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
    created_at: datetime | None = Field(default_factory=datetime.utcnow)
