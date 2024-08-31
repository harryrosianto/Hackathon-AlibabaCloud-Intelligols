
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.bean_type import BeanType
from schemas.bean_type import BeanTypeCreateSch, BeanTypeUpdateSch

class CRUDBeanType(CRUDBase[BeanType, BeanTypeCreateSch, BeanTypeUpdateSch]):    
    pass

bean_type = CRUDBeanType(BeanType)
