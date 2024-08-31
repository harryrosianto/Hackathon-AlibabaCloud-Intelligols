from datetime import datetime
from fastapi import HTTPException
from typing import Any, Dict, Generic, List, Type, TypeVar
from uuid import UUID
from schemas.common import OrderEnumSch
from fastapi_pagination.ext.sqlmodel import paginate
from fastapi_async_sqlalchemy import db
from fastapi_pagination import Params, Page
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlmodel import SQLModel, select, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel.sql.expression import Select
from sqlalchemy import exc

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
SchemaType = TypeVar("SchemaType", bound=BaseModel)
T = TypeVar("T", bound=SQLModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLModel model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(
        self, *, id: int | str | None = None, uuid: UUID | None = None, db_session: AsyncSession | None = None
    ) -> ModelType | None:
        db_session = db_session or db.session
        if id:
            query = select(self.model).where(self.model.id == id)
        if uuid:
            query = select(self.model).where(self.model.uuid == uuid)
        response = await db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_by_ids(
        self,
        *,
        list_ids: List[UUID | str | int],
        db_session: AsyncSession | None = None,
    ) -> List[ModelType] | None:
        db_session = db_session or db.session
        response = await db_session.execute(
            select(self.model).where(self.model.id.in_(list_ids))
        )
        return response.scalars().all()

    async def get_count(
        self, db_session: AsyncSession | None = None
    ) -> ModelType | None:
        db_session = db_session or db.session
        response = await db_session.execute(
            select(func.count()).select_from(select(self.model).subquery())
        )
        return response.scalar_one()

    async def get_multi(
        self,
        *,
        skip: int = 0,
        limit: int = 100,
        query: T | Select[T] | None = None,
        db_session: AsyncSession | None = None,
    ) -> List[ModelType]:
        db_session = db_session or db.session
        if query is None:
            query = select(self.model).offset(
                skip).limit(limit).order_by(self.model.id)
        response = await db_session.execute(query)
        return response.scalars().all()

    async def get_multi_paginated(
        self,
        *,
        params: Params | None = Params(),
        query: T | Select[T] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        db_session = db_session or db.session
        if query is None:
            query = select(self.model)
        return await paginate(db_session, query, params)

    async def get_multi_paginated_ordered(
        self,
        *,
        params: Params | None = Params(),
        order_by: str | None = None,
        order: OrderEnumSch | None = OrderEnumSch.ascendent,
        query: T | Select[T] | None = None,
        db_session: AsyncSession | None = None,
    ) -> Page[ModelType]:
        db_session = db_session or db.session

        columns = self.model.__table__.columns

        if order_by not in columns or order_by is None:
            order_by = self.model.id

        if query is not None:
            if order == OrderEnumSch.ascendent:
                query = query.order_by(columns[order_by].asc())

            else:
                query = query.order_by(columns[order_by].desc())
        else:
            if order == OrderEnumSch.ascendent:
                query = select(self.model).order_by(columns[order_by].asc())
            else:
                query = select(self.model).order_by(columns[order_by].desc())

        return await paginate(db_session, query, params)

    async def get_multi_ordered(
        self,
        *,
        order_by: str | None = None,
        order: OrderEnumSch | None = OrderEnumSch.ascendent,
        skip: int = 0,
        limit: int = 100,
        db_session: AsyncSession | None = None,
    ) -> List[ModelType]:
        db_session = db_session or db.session

        columns = self.model.__table__.columns

        if order_by not in columns or order_by is None:
            order_by = self.model.id

        if order == OrderEnumSch.ascendent:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by.value].asc())
            )
        else:
            query = (
                select(self.model)
                .offset(skip)
                .limit(limit)
                .order_by(columns[order_by.value].desc())
            )

        response = await db_session.execute(query)
        return response.scalars().all()

    async def create(
        self,
        *,
        obj_in: CreateSchemaType | ModelType,
        created_by_id: UUID | str | None = None,
        db_session: AsyncSession | None = None,
        with_commit: bool | None = True
    ) -> ModelType:
        db_session = db_session or db.session
        db_obj = self.model.from_orm(obj_in)  # type: ignore
        if created_by_id:
            db_obj.created_by_id = created_by_id

        try:
            db_session.add(db_obj)
            if with_commit:
                await db_session.commit()
                await db_session.refresh(db_obj)
        except exc.IntegrityError:
            db_session.rollback()
            raise HTTPException(
                status_code=409,
                detail="Resource already exists",
            )
        return db_obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        obj_new: UpdateSchemaType | Dict[str, Any] | ModelType,
        db_session: AsyncSession | None = None,
        with_commit: bool | None = True
    ) -> ModelType:
        db_session = db_session or db.session
        obj_data = jsonable_encoder(obj_current)

        if isinstance(obj_new, dict):
            update_data = obj_new
        else:
            update_data = obj_new.dict(
                exclude_unset=True
            )  # This tells Pydantic to not include the values that were not sent
        for field in obj_data:
            if field in update_data:
                setattr(obj_current, field, update_data[field])

        db_session.add(obj_current)
        if with_commit:
            await db_session.commit()
            await db_session.refresh(obj_current)
        return obj_current

    async def remove(
        self, *, id: int | str | None = None, uuid: UUID | None = None, db_session: AsyncSession | None = None
    ) -> ModelType:
        db_session = db_session or db.session

        if id:
            response = await db_session.execute(
                select(self.model).where(self.model.id == id)
            )
        if uuid:
            response = await db_session.execute(
                select(self.model).where(self.model.uuid == uuid)
            )
        obj = response.scalar_one()
        await db_session.delete(obj)
        await db_session.commit()
        return obj

    async def get_all_ordered(
        self,
        *,
        query: T | Select[T] | None = None,
        order_by: str | None = None,
        order: OrderEnumSch | None = OrderEnumSch.ascendent,
        db_session: AsyncSession | None = None,
    ) -> list[ModelType]:
        db_session = db_session or db.session

        columns = self.model.__table__.columns

        if order_by not in columns or order_by is None:
            raise HTTPException(
                status_code=404,
                detail='order_by not in table'
            )

        if query is not None:
            if order == OrderEnumSch.ascendent:
                query = query.order_by(columns[order_by].asc())

            else:
                query = query.order_by(columns[order_by].desc())
        else:
            if order == OrderEnumSch.ascendent:

                query = (
                    select(self.model)
                    .order_by(columns[order_by].asc())
                )
            else:
                query = (
                    select(self.model)
                    .order_by(columns[order_by].desc())
                )

        response = await db_session.execute(query)
        return response.scalars().all()

    async def get_list(
        self,
        *,
        query: T | Select[T] | None = None,
        order_by: str | None = None,
        order: OrderEnumSch | None = OrderEnumSch.ascendent,
        db_session: AsyncSession | None = None,
    ) -> list[ModelType]:
        db_session = db_session or db.session

        columns = self.model.__table__.columns

        if order_by not in columns or order_by is None:
            raise HTTPException(
                status_code=404,
                detail='order_by not in table'
            )

        if query is not None:
            if order == OrderEnumSch.ascendent:
                query = query.order_by(columns[order_by].asc())

            else:
                query = query.order_by(columns[order_by].desc())
        else:
            if order == OrderEnumSch.ascendent:

                query = (
                    select(self.model)
                    .order_by(columns[order_by].asc())
                )
            else:
                query = (
                    select(self.model)
                    .order_by(columns[order_by].desc())
                )

        response = await db_session.execute(query)
        return response.all()
