
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.farming_info import FarmingInfo
from schemas.farming_info import FarmingInfoCreateSch, FarmingInfoUpdateSch

class CRUDFarmingInfo(CRUDBase[FarmingInfo, FarmingInfoCreateSch, FarmingInfoUpdateSch]):    
    pass

farming_info = CRUDFarmingInfo(FarmingInfo)
