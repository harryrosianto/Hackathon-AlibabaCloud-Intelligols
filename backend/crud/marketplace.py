
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.marketplace import Marketplace
from schemas.marketplace import MarketplaceCreateSch, MarketplaceUpdateSch

class CRUDMarketplace(CRUDBase[Marketplace, MarketplaceCreateSch, MarketplaceUpdateSch]):    
    pass

marketplace = CRUDMarketplace(Marketplace)
