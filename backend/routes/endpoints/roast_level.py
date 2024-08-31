from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.roast_level import RoastLevel
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.roast_level import RoastLevelCreateSch, RoastLevelSch, RoastLevelUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of roast_levels
    """
    objs = await crud.roast_level.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[RoastLevelSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.roast_level.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[RoastLevelSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.roast_level.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(RoastLevel, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: RoastLevelCreateSch
):
    """
    Create a new roast_level
    """
    # obj_current = await crud.roast_level.get_by_name(name=sch.name)
    # if obj_current:
    #     raise NameExistException(RoastLevel, name=obj_current.name)

    new_obj = await crud.roast_level.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[RoastLevelSch])
async def update(
    id: str,
    sch: RoastLevelUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.roast_level.get(id=id)
    if not obj_current:
        raise IdNotFoundException(RoastLevel, id)
    # name = await crud.roast_level.get_by_name(name=sch.name)
    # if name:
    #     raise NameExistException(RoastLevel, sch.name)
    obj_updated = await crud.roast_level.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
