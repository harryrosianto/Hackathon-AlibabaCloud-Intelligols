from sqlmodel import Field, Relationship, SQLModel
from models.model import BaseEntryModel
from models.user import User

class BeanQualityBase(SQLModel):
    bean_type_id: str =Field(nullable=False, foreign_key="bean_type.id")
    altitude: float = Field(nullable=False)
    weather_temperature: float = Field(nullable=False)
    weather_rainfall: float = Field(nullable=False)
    humidity: float = Field(nullable=False)
    soil_ph: float = Field(nullable=False)
    soil_texture: str = Field(nullable=False)
    plant_age: float = Field(nullable=False)
    disease: str | None = Field(nullable=True, max_length=255)

class BeanQualityFullBase(BeanQualityBase, BaseEntryModel):
    pass

class BeanQuality(BeanQualityFullBase, table=True):
    pass

    # user: "User" = Relationship(back_populates="beanqualitys",sa_relationship_kwargs={
    #         "lazy": "joined",
    #         "primaryjoin": "BeanQuality.farmer_id==User.id",
    #     })