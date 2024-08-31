from fastapi import APIRouter
from routes.endpoints import register, analysis, bean_quality, bean_type, buyer_preferences, disease_management, farming_info, growth, marketplace, roast_level, user, role

api_router = APIRouter()
api_router.include_router(register.router, prefix="/register", tags=["register"])

api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(bean_quality.router, prefix="/bean_quality", tags=["bean_quality"])
api_router.include_router(bean_type.router, prefix="/bean_type", tags=["bean_type"])
api_router.include_router(buyer_preferences.router, prefix="/buyer_preferences", tags=["buyer_preferences"])
api_router.include_router(disease_management.router, prefix="/disease_management", tags=["disease_management"])
api_router.include_router(farming_info.router, prefix="/farming_info", tags=["farming_info"])
api_router.include_router(growth.router, prefix="/growth", tags=["growth"])
api_router.include_router(roast_level.router, prefix="/roast_level", tags=["roast_level"])
api_router.include_router(role.router, prefix="/role", tags=["role"])
api_router.include_router(user.router, prefix="/user", tags=["user"])