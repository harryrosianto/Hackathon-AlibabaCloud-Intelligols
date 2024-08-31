from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class AnalysisBase(SQLModel):
    title: str = Field(nullable=False, max_length=50)
    descs: str | None = Field(nullable=True, max_length=255)
    image: str | None = Field(nullable=True)

class AnalysisFullBase(AnalysisBase, BaseEntryModel):
    pass

class Analysis(AnalysisFullBase, table=True):
    pass
