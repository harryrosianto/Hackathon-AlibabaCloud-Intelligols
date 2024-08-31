from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.farming_info import FarmingInfo
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.farming_info import FarmingInfoCreateSch, FarmingInfoSch, FarmingInfoUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of farming_infos
    """
    objs = await crud.farming_info.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[FarmingInfoSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.farming_info.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[FarmingInfoSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.farming_info.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(FarmingInfo, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: FarmingInfoCreateSch
):
    """
    Create a new farming_info
    """
    # obj_current = await crud.farming_info.get_by_name(name=sch.name)
    # if obj_current:
    #     raise NameExistException(FarmingInfo, name=obj_current.name)

    new_obj = await crud.farming_info.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[FarmingInfoSch])
async def update(
    id: str,
    sch: FarmingInfoUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.farming_info.get(id=id)
    if not obj_current:
        raise IdNotFoundException(FarmingInfo, id)
    # name = await crud.farming_info.get_by_name(name=sch.name)
    # if name:
    #     raise NameExistException(FarmingInfo, sch.name)
    obj_updated = await crud.farming_info.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
