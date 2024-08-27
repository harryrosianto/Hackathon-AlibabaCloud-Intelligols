import math
from fastapi_pagination import Params
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_
from sqlmodel import SQLModel
from typing import Generic, TypeVar, Type, List, Optional, Any
from fastapi import Query
from pydantic import BaseModel

from schemas.response import GetResponsePaginatedSch, PageBase
from util.exception import NotFoundError
from schemas.common import OrderEnumSch

T = TypeVar('T', bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[T, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[T]):
        self.model = model

    async def create(self, db: AsyncSession, obj_in: CreateSchemaType) -> T:
        db_obj = self.model.from_orm(obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get(self, db: AsyncSession, id: Any) -> Optional[T]:
        statement = select(self.model).where(self.model.id == id)
        results = await db.execute(statement)
        return results.scalar_one_or_none()

    async def get_multi_paginated_ordered(
        self,
        db: AsyncSession,
        *,
        params: Params,
        query: Any = None,
        order_by: str = 'id',
        order: OrderEnumSch = OrderEnumSch.ascendent
    ) -> GetResponsePaginatedSch[T]:
        if query is None:
            query = select(self.model)
        total = await db.scalar(select(func.count()).select_from(query.subquery()))
        if order == OrderEnumSch.ascendent:
            query = query.order_by(getattr(self.model, order_by).asc())
        else:
            query = query.order_by(getattr(self.model, order_by).desc())
        query = query.offset(params.size * params.page).limit(params.size)
        results = await db.execute(query)
        objs = results.scalars().all()
        
        # Buat objek PageBase
        page_base = PageBase(
            items=objs,
            page=params.page,
            size=params.size,
            total=total,
            pages=math.ceil(total / params.size),
            next_page=params.page + 1 if params.page < math.ceil(total / params.size) else None,
            previous_page=params.page - 1 if params.page > 1 else None,
        )
        
        # Buat dan kembalikan GetResponsePaginatedSch
        return GetResponsePaginatedSch[T](
            message="Data got correctly",
            meta={},
            data=page_base
        )

    async def get_all_ordered(
        self,
        db: AsyncSession,
        *,
        order_by: str = 'id',
        order: OrderEnumSch = OrderEnumSch.ascendent
    ) -> List[T]:
        query = select(self.model)

        if order == OrderEnumSch.ascendent:
            query = query.order_by(getattr(self.model, order_by).asc())
        else:
            query = query.order_by(getattr(self.model, order_by).desc())

        results = await db.execute(query)
        return results.scalars().all()

    async def update(self, db: AsyncSession, *, db_obj: T, obj_in: UpdateSchemaType) -> T:
        obj_data = db_obj.dict()
        update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: Any) -> T:
        obj = await self.get(db, id)
        if obj is None:
            raise NotFoundError(f"{self.model.__name__} with id {id} not found")
        await db.delete(obj)
        await db.commit()
        return obj

    async def search(self, db: AsyncSession, *, search: str, search_fields: List[str]) -> List[T]:
        conditions = [getattr(self.model, field).ilike(f"%{search}%") for field in search_fields]
        query = select(self.model).filter(or_(*conditions)).distinct()
        results = await db.execute(query)
        return results.scalars().all()