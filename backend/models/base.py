from datetime import datetime, timezone
from sqlmodel import SQLModel as _SQLModel, Field
from sqlalchemy.orm import declared_attr
from stringcase import snakecase
import ulid
from sqlalchemy import Column
from sqlalchemy.sql import func
from util.tz_datetime import TZDateTime

class SQLModel(_SQLModel):
    @declared_attr  # type: ignore
    def __tablename__(cls) -> str:
        return snakecase(cls.__name__)

def generate_ulid() -> str:
    return str(ulid.new())

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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # Define columns directly with SQLAlchemy for automatic timestamp management
    @declared_attr
    def created_at(cls) -> Column:
        return Column(TZDateTime, nullable=False, default=datetime.now(timezone.utc))

    @declared_attr
    def updated_at(cls) -> Column:
        return Column(TZDateTime, nullable=False, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
