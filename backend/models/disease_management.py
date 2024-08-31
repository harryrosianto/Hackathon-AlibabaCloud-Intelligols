from sqlmodel import Field, SQLModel

from models.model import BaseEntryModel


class DiseaseManagementBase(SQLModel):
    bean_type_id: str =Field(nullable=False, foreign_key="bean_type.id")
    plant_age: float = Field(nullable=False)
    observed_symptoms: str = Field(nullable=False, max_length=100)
    affected_parts: str = Field(nullable=False, max_length=100)
    pest_presence: str | None= Field(nullable=True, max_length=100)
    disease_identification: str | None = Field(nullable=True, max_length=100)
    pest_control_methods: str | None = Field(nullable=True, max_length=100)
    disease_management_methods: str | None = Field(nullable=True, max_length=100)
    climate_conditions: str | None = Field(nullable=True, max_length=100)
    watering_practices: str | None = Field(nullable=True, max_length=100)
    fertilizer_use: str | None = Field(nullable=True, max_length=100)
    soil_condition: str | None = Field(nullable=True, max_length=100)
    budget: float = Field(nullable=False, default=0)
    available_resources: str | None = Field(nullable=True, max_length=255)

class DiseaseManagementFullBase(DiseaseManagementBase, BaseEntryModel):
    pass

class DiseaseManagement(DiseaseManagementFullBase, table=True):
    pass
