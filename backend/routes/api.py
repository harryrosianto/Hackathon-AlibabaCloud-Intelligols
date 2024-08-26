from fastapi import APIRouter
from routes.endpoints import user

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
# api_router.include_router(product.router, prefix="/product", tags=["product"])
