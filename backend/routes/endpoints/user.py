from fastapi import APIRouter, Depends, status, Query, UploadFile, File
from fastapi_pagination import Params
from crud.crud import CRUDBase
from models.user import User
from schemas.common import OrderEnumSch
from schemas.response import GetResponseBaseSch, GetResponsePaginatedSch, PostResponseBaseSch, PutResponseBaseSch, create_response
from schemas.user import UserCreateSch, UserSch, UserUpdateSch
from util.exception import IdNotFoundException, NameExistException
from sqlmodel import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from util.database import get_session
import crud

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[UserSch])
async def get(
    db: AsyncSession = Depends(get_session),
    params: Params = Depends(),
    search: str = Query(description="Search user by name", default=None)
):
    """
    Gets a paginated list objects
    """
    query = select(User)
    if search:
        query = query.filter(
            or_(
                User.name.ilike(f"%{search}%"),
            )
        ).distinct()
    objs = await crud.user.get_multi_paginated_ordered(db, params=params, query=query, order_by='name', order=OrderEnumSch.ascendent)
    res = create_response(data=objs)
    return res

@router.get("/no_page", response_model=GetResponseBaseSch[list[UserSch]])
async def get_no_page(
    db: AsyncSession = Depends(get_session),
):
    """
    Gets a list objects
    """
    objs = await crud.user.get_all_ordered(db, order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[UserSch])
async def get_by_id(
    id: str,
    db: AsyncSession = Depends(get_session),
):
    """
    Gets an object by its id
    """
    obj = await crud.user.get(db, id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(User, id)


@router.post(
    "",
    response_model=PostResponseBaseSch[UserSch],
    status_code=status.HTTP_201_CREATED,
)
async def create(
    sch: UserCreateSch,
    db: AsyncSession = Depends(get_session),
):
    """
    Creates a new obj
    """
    obj_current = await crud.user.get_by_username(usn=sch.username)
    if obj_current:
        raise NameExistException(User, sch.username)
    new_obj = await crud.user.create(db, obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[UserSch])
async def update(
    id: str,
    sch: UserUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.user.get(id=id)
    if not obj_current:
        raise IdNotFoundException(User, id)
    name = await crud.user.get_by_name(name=sch.name)
    if name:
        raise NameExistException(User, sch.name)
    obj_updated = await crud.user.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
