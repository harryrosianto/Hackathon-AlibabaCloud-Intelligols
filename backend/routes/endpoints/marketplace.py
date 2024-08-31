from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.marketplace import Marketplace
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.marketplace import MarketplaceCreateSch, MarketplaceSch, MarketplaceUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of marketplaces
    """
    objs = await crud.marketplace.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[MarketplaceSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.marketplace.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[MarketplaceSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.marketplace.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(Marketplace, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: MarketplaceCreateSch
):
    """
    Create a new marketplace
    """
    obj_current = await crud.marketplace.get_by_name(name=sch.name)
    if obj_current:
        raise NameExistException(Marketplace, name=obj_current.name)

    new_obj = await crud.marketplace.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[MarketplaceSch])
async def update(
    id: str,
    sch: MarketplaceUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.marketplace.get(id=id)
    if not obj_current:
        raise IdNotFoundException(Marketplace, id)
    name = await crud.marketplace.get_by_name(name=sch.name)
    if name:
        raise NameExistException(Marketplace, sch.name)
    obj_updated = await crud.marketplace.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
