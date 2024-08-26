
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.base import CRUDBase
from models import User
from fastapi_async_sqlalchemy import db

from schemas.user import UserCreateSch, UserUpdateSch

class CRUDUser(CRUDBase[User, UserCreateSch, UserUpdateSch]):    
    async def get_by_username(self, *, usn, db_session: AsyncSession | None = None) -> User:
        db_session = db_session or db.session
        response = await db_session.exec(select(User).where(User.username == usn))
        return response.scalar_one_or_none()

user = CRUDUser(User)
