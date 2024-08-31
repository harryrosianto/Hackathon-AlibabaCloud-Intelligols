from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.growth import Growth
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.growth import GrowthCreateSch, GrowthSch, GrowthUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of growths
    """
    objs = await crud.growth.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[GrowthSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.growth.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[GrowthSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.growth.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(Growth, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: GrowthCreateSch
):
    """
    Create a new growth
    """
    # obj_current = await crud.growth.get_by_name(name=sch.name)
    # if obj_current:
    #     raise NameExistException(Growth, name=obj_current.name)

    new_obj = await crud.growth.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[GrowthSch])
async def update(
    id: str,
    sch: GrowthUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.growth.get(id=id)
    if not obj_current:
        raise IdNotFoundException(Growth, id)
    # name = await crud.growth.get_by_name(name=sch.name)
    # if name:
    #     raise NameExistException(Growth, sch.name)
    obj_updated = await crud.growth.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
