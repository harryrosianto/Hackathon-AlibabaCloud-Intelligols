
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.product import Product
from schemas.product import ProductCreateSch, ProductUpdateSch

class CRUDProduct(CRUDBase[Product, ProductCreateSch, ProductUpdateSch]):    
    async def get_by_name(self, *, name, db_session: AsyncSession | None = None) -> Product:
        db_session = db_session or db.session
        response = await db_session.execute(select(Product).where(Product.name == name))
        return response.scalar_one_or_none()

product = CRUDProduct(Product)
