from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.bean_quality import BeanQuality
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.bean_quality import BeanQualityCreateSch, BeanQualitySch, BeanQualityUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of bean_qualitys
    """
    objs = await crud.bean_quality.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[BeanQualitySch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.bean_quality.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[BeanQualitySch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.bean_quality.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(BeanQuality, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: BeanQualityCreateSch
):
    """
    Create a new bean_quality
    """
    # obj_current = await crud.bean_quality.get_by_name(name=sch.name)
    # if obj_current:
    #     raise NameExistException(BeanQuality, name=obj_current.name)

    new_obj = await crud.bean_quality.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[BeanQualitySch])
async def update(
    id: str,
    sch: BeanQualityUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.bean_quality.get(id=id)
    if not obj_current:
        raise IdNotFoundException(BeanQuality, id)
    # name = await crud.bean_quality.get_by_name(name=sch.name)
    # if name:
    #     raise NameExistException(BeanQuality, sch.name)
    obj_updated = await crud.bean_quality.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
