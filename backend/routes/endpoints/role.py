from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.role import Role
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.role import RoleCreateSch, RoleSch, RoleUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of roles
    """
    objs = await crud.role.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[RoleSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.role.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[RoleSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.role.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(Role, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: RoleCreateSch
):
    """
    Create a new role
    """
    obj_current = await crud.role.get_by_name(name=sch.name)
    if obj_current:
        raise NameExistException(Role, name=obj_current.name)

    new_obj = await crud.role.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[RoleSch])
async def update(
    id: str,
    sch: RoleUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.role.get(id=id)
    if not obj_current:
        raise IdNotFoundException(Role, id)
    name = await crud.role.get_by_name(name=sch.name)
    if name:
        raise NameExistException(Role, sch.name)
    obj_updated = await crud.role.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
