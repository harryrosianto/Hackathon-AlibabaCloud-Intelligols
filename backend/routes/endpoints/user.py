from fastapi import APIRouter, Depends, status, Query
from fastapi_pagination import Params
from models.user import User
from schemas.common import OrderEnumSch
from schemas.response import GetResponseBaseSch, GetResponsePaginatedSch, PostResponseBaseSch, PutResponseBaseSch, create_response
from schemas.user import UserCreateSch, UserSch, UserUpdateSch
from util.exception import IdNotFoundException, NameExistException
from sqlmodel import select, or_
import crud

router = APIRouter()

@router.get("", response_model=GetResponsePaginatedSch[UserSch])
async def get(
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
    objs = await crud.user.get_multi_paginated_ordered(params=params, query=query, order_by='name', order=OrderEnumSch.ascendent)
    res = create_response(data=objs)
    return res

@router.get("/no_page", response_model=GetResponseBaseSch[list[UserSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.user.get_all_ordered(order_by='id')
    return create_response(data=objs)

# @router.get("/myprofile")
# async def get_my_data(
#     current_user: User = Depends(deps.get_current_user()),
# ) -> IGetResponseBase[IUserRead]:
#     """
#     Gets my user profile information
#     """
#     return create_response(data=current_user)

@router.get("/{id}", response_model=GetResponseBaseSch[UserSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.user.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(User, id)

# @router.post(
#     "",
#     response_model=PostResponseBaseSch[UserSch],
#     status_code=status.HTTP_201_CREATED,
# )
# async def create(
#     sch: UserCreateSch,
# ):
#     """
#     Creates a new obj
#     """
#     obj_current = await crud.user.get_by_email(email=sch.email)
#     if obj_current:
#         raise NameExistException(User, sch.username)
#     new_obj = await crud.user.create(obj_in=sch)
#     return create_response(data=new_obj)

# @router.put("/myprofile", response_model=PutResponseBaseSch[UserSch])
# async def update(
#     id: str,
#     sch: UserUpdateSch
# ):
#     """
#     Updates a obj by its id
#     """
#     obj_current = await crud.user.get(id=id)
#     if not obj_current:
#         raise IdNotFoundException(User, id)
#     name = await crud.user.get_by_username(usn=sch.username)
#     if name:
#         raise NameExistException(User, sch.username)
#     obj_updated = await crud.user.update(obj_current=obj_current, obj_new=sch)
#     return create_response(data=obj_updated)

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
    name = await crud.user.get_by_username(usn=sch.username)
    if name:
        raise NameExistException(User, sch.username)
    obj_updated = await crud.user.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
