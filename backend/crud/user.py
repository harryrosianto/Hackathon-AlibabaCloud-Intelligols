from typing import Any
from fastapi import HTTPException
from pydantic import EmailStr
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from config.security import get_password_hash, verify_password
from crud.crud import CRUDBase
from models.user import User
from fastapi_async_sqlalchemy import db
from sqlalchemy import exc

from schemas.user import UserCreateSch, UserUpdateSch

class CRUDUser(CRUDBase[User, UserCreateSch, UserUpdateSch]):    
    async def get_by_email(self, *, email, db_session: AsyncSession | None = None) -> User:
        db_session = db_session or db.session
        response = await db_session.execute(select(User).where(User.email == email))
        return response.scalar_one_or_none()
    
    async def create_with_role(
        self, *, obj_in: UserCreateSch, db_session: AsyncSession | None = None
    ) -> User:
        db_session = db_session or db.session
        db_obj = User.model_validate(obj_in)
        db_obj.hashed_password = get_password_hash(obj_in.password)
        try:
            db_session.add(db_obj)
            await db_session.commit()
            await db_session.refresh(db_obj)
        except exc.IntegrityError:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        return db_obj
    
    async def authenticate(self, *, email: EmailStr, password: str) -> User | None:
        user = await self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    async def get_by_id_active(self, *, id: str) -> User | None:
        user = await super().get(id=id)
        if not user:
            return None
        if user.is_active is False:
            return None

        return user
    
    async def update_is_active(
        self, *, db_obj: list[User], obj_in: int | str | dict[str, Any]
    ) -> User | None:
        response = None
        db_session = super().get_db().session
        for x in db_obj:
            x.is_active = obj_in.is_active
            db_session.add(x)
            await db_session.commit()
            await db_session.refresh(x)
            response.append(x)
        return response

user = CRUDUser(User)
