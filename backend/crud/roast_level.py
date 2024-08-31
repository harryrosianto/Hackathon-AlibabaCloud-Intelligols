
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.roast_level import RoastLevel
from schemas.roast_level import RoastLevelCreateSch, RoastLevelUpdateSch

class CRUDRoastLevel(CRUDBase[RoastLevel, RoastLevelCreateSch, RoastLevelUpdateSch]):    
    pass

roast_level = CRUDRoastLevel(RoastLevel)
