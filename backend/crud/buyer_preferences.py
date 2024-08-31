
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.buyer_preferences import BuyerPreferences
from schemas.buyer_preferences import BuyerPreferencesCreateSch, BuyerPreferencesUpdateSch

class CRUDBuyerPreferences(CRUDBase[BuyerPreferences, BuyerPreferencesCreateSch, BuyerPreferencesUpdateSch]):    
    pass

buyer_preferences = CRUDBuyerPreferences(BuyerPreferences)
