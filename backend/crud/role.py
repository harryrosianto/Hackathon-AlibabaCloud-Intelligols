from fastapi import HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from crud.crud import CRUDBase
from models.role import Role
from fastapi_async_sqlalchemy import db
from sqlalchemy import exc
from models.user import User
from schemas.role import RoleCreateSch, RoleUpdateSch

class CRUDRole(CRUDBase[Role, RoleCreateSch, RoleUpdateSch]):    
    async def get_by_name(self, *, name, db_session: AsyncSession | None = None) -> Role:
        db_session = db_session or db.session
        response = await db_session.execute(select(Role).where(Role.name == name))
        return response.scalar_one_or_none()
    
    async def add_role_to_user(self, *, user: User, role_id: str) -> Role:
        db_session = super().get_db().session
        role = await super().get(id=role_id)
        role.users.append(user)
        try:
            db_session.add(role)
            await db_session.commit()
            await db_session.refresh(role)
        except exc.IntegrityError:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        return role

role = CRUDRole(Role)
