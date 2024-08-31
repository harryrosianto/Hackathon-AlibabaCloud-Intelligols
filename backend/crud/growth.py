
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.growth import Growth
from schemas.growth import GrowthCreateSch, GrowthUpdateSch

class CRUDGrowth(CRUDBase[Growth, GrowthCreateSch, GrowthUpdateSch]):    
    pass

growth = CRUDGrowth(Growth)
