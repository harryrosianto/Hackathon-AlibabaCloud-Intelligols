
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.bean_quality import BeanQuality
from schemas.bean_quality import BeanQualityCreateSch, BeanQualityUpdateSch

class CRUDBeanQuality(CRUDBase[BeanQuality, BeanQualityCreateSch, BeanQualityUpdateSch]):    
    pass

bean_quality = CRUDBeanQuality(BeanQuality)
