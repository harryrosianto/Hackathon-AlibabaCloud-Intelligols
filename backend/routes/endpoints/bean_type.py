from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.bean_type import BeanType
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.bean_type import BeanTypeCreateSch, BeanTypeSch, BeanTypeUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of bean_types
    """
    objs = await crud.bean_type.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[BeanTypeSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.bean_type.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[BeanTypeSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.bean_type.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(BeanType, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: BeanTypeCreateSch
):
    """
    Create a new bean_type
    """
    # obj_current = await crud.bean_type.get_by_name(name=sch.name)
    # if obj_current:
    #     raise NameExistException(BeanType, name=obj_current.name)

    new_obj = await crud.bean_type.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[BeanTypeSch])
async def update(
    id: str,
    sch: BeanTypeUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.bean_type.get(id=id)
    if not obj_current:
        raise IdNotFoundException(BeanType, id)
    # name = await crud.bean_type.get_by_name(name=sch.name)
    # if name:
    #     raise NameExistException(BeanType, sch.name)
    obj_updated = await crud.bean_type.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
