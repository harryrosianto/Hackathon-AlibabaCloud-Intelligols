from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.buyer_preferences import BuyerPreferences
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.buyer_preferences import BuyerPreferencesCreateSch, BuyerPreferencesSch, BuyerPreferencesUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of buyer_preferencess
    """
    objs = await crud.buyer_preferences.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[BuyerPreferencesSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.buyer_preferences.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[BuyerPreferencesSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.buyer_preferences.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(BuyerPreferences, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: BuyerPreferencesCreateSch
):
    """
    Create a new buyer_preferences
    """
    # obj_current = await crud.buyer_preferences.get_by_name(name=sch.name)
    # if obj_current:
    #     raise NameExistException(BuyerPreferences, name=obj_current.name)

    new_obj = await crud.buyer_preferences.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[BuyerPreferencesSch])
async def update(
    id: str,
    sch: BuyerPreferencesUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.buyer_preferences.get(id=id)
    if not obj_current:
        raise IdNotFoundException(BuyerPreferences, id)
    # name = await crud.buyer_preferences.get_by_name(name=sch.name)
    # if name:
    #     raise NameExistException(BuyerPreferences, sch.name)
    obj_updated = await crud.buyer_preferences.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
