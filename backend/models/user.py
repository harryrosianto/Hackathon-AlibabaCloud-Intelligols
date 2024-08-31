from datetime import datetime
from pydantic import EmailStr, field_validator
from sqlmodel import Field, Relationship, SQLModel, Column, String, DateTime
from typing import TYPE_CHECKING
from models.model import BaseEntryModel
from models.role import Role
from schemas.common import GenderEnum

if TYPE_CHECKING:
    from .bean_quality import BeanQuality

class UserBase(SQLModel):
    username: str = Field(nullable=False, max_length=50, unique=True)
    name: str = Field(nullable=False, max_length=255)
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    birthdate: datetime | None = Field(
        default=None, sa_column=Column(DateTime(timezone=True), nullable=True)
    )  # birthday with timezone
    role_id: str = Field(nullable=False, foreign_key="role.id")
    is_active: bool = Field(nullable=False, default=True)
    phone: str | None = None
    gender: GenderEnum | None = Field(
        default=GenderEnum.other
    )
    state: str | None = None
    country: str | None = None
    address: str | None = None
    
    # @field_validator('username')
    # def validate_code(cls, value):
    #     return value.lower()
    
    # @field_validator('name')
    # def validate_code(cls, value):
    #     return value.title()

class UserFullBase(BaseEntryModel, UserBase):
    hashed_password: str | None = Field(default=None, nullable=False, index=True)

class User(UserFullBase, table=True):
    # beanqualitys: list['BeanQuality'] | None = Relationship(back_populates='user',  sa_relationship_kwargs={
    #     'lazy': 'selectin',
    #     'foreign_keys': 'BeanQuality.farmer_id'
    # })
    role: Role = Relationship(  # noqa: F821
        back_populates="users", sa_relationship_kwargs={"lazy": "joined"}
    )

    
    
# from pydantic import BaseModel
# from typing import Optional, List
# from datetime import datetime

# # User model
# class User(BaseModel):
#     id: int
#     username: str
#     full_name: Optional[str] = None
#     email: str
#     role: str  # Could be 'farmer', 'buyer', or 'admin'
#     disabled: Optional[bool] = None
#     created_at: datetime

# # Coffee BeanQuality model
# class CoffeeBeanQuality(BaseModel):
#     id: int
#     name: str
#     variety: str
#     quality: str
#     price: float
#     farmer_id: int
#     description: Optional[str] = None
#     created_at: datetime

# # Environmental Data model
# class EnvironmentalData(BaseModel):
#     id: int
#     farmer_id: int
#     soil_condition: str
#     weather: str
#     geography: str
#     created_at: datetime

# # AI Recommendation model
# class AIRecommendation(BaseModel):
#     id: int
#     farmer_id: int
#     environmental_data_id: int
#     recommendation: str
#     justification: str
#     created_at: datetime

# # Farmer's Dashboard model
# class FarmersDashboard(BaseModel):
#     farmer_id: int
#     environmental_data: List[EnvironmentalData]
#     ai_recommendations: List[AIRecommendation]
#     production_tracking: List[dict]  # Placeholder for actual production tracking data
#     communication_tools: List[dict]  # Placeholder for communication data

# # Buyer's Dashboard model
# class BuyersDashboard(BaseModel):
#     buyer_id: int
#     production_monitoring: List[CoffeeBeanQuality]
#     pricing_information: List[dict]  # Placeholder for actual pricing data
#     transaction_management: List[dict]  # Placeholder for transaction data
#     communication_tools: List[dict]  # Placeholder for communication data

# # AI Analysis model
# class AIAnalysis(BaseModel):
#     farmer_id: int
#     environmental_data_summary: List[EnvironmentalData]
#     ai_recommendations: List[AIRecommendation]
#     graphs_visualizations: List[dict]  # Placeholder for graph and visualization data

# # Market Place model
# class Marketplace(BaseModel):
#     id: int
#     coffee_listings: List[CoffeeBeanQuality]
#     search_filter: List[dict]  # Placeholder for search and filter criteria
#     purchase_options: List[dict]  # Placeholder for purchase data
#     ratings_reviews: List[dict]  # Placeholder for rating and review data

# # Knowledge Base / Resources model
# class KnowledgeBase(BaseModel):
#     id: int
#     farming_guides: List[dict]  # Placeholder for farming guide content
#     ai_in_agriculture: List[dict]  # Placeholder for AI in agriculture content
#     faqs: List[dict]  # Placeholder for FAQ content

# # Contact Us model
# class ContactUs(BaseModel):
#     id: int
#     email: str
#     phone: Optional[str] = None
#     message: str
#     created_at: datetime

# # User Account model
# class UserAccount(BaseModel):
#     id: int
#     user: User
#     profile_management: dict  # Placeholder for profile management data
#     notification_settings: dict  # Placeholder for notification settings data
#     subscription_management: Optional[dict] = None  # Placeholder for subscription data

# # Admin Dashboard model
# class AdminDashboard(BaseModel):
#     admin_id: int
#     user_management: List[User]
#     content_management: List[dict]  # Placeholder for content management data
#     data_analytics: List[dict]  # Placeholder for analytics data

# # Login / Sign Up model
# class AuthModel(BaseModel):
#     username: str
#     password: str
#     role: str  # Could be 'farmer', 'buyer', or 'admin'
