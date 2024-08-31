from fastapi import APIRouter, Depends, status
from fastapi_pagination import Params

import crud
from models.analysis import Analysis
from schemas.response import GetResponseBaseSch, PutResponseBaseSch, create_response
from schemas.analysis import AnalysisCreateSch, AnalysisSch, AnalysisUpdateSch
from util.exception import IdNotFoundException, NameExistException


router = APIRouter()

@router.get("")
async def get(
    params: Params = Depends(),
):
    """
    Gets a paginated list of analysis
    """
    objs = await crud.analysis.get_multi_paginated(params=params)
    return create_response(data=objs)


@router.get("/no_page", response_model=GetResponseBaseSch[list[AnalysisSch]])
async def get_no_page(
):
    """
    Gets a list objects
    """
    objs = await crud.analysis.get_all_ordered(order_by='id')
    return create_response(data=objs)


@router.get("/{id}", response_model=GetResponseBaseSch[AnalysisSch])
async def get_by_id(
    id: str,
):
    """
    Gets an object by its id
    """
    obj = await crud.analysis.get(id=id)
    if obj:
        return create_response(data=obj)
    else:
        raise IdNotFoundException(Analysis, id)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create(
    sch: AnalysisCreateSch
):
    """
    Create a new analysis
    """
    # obj_current = await crud.analysis.get_by_name(name=sch.name)
    # if obj_current:
    #     raise NameExistException(Analysis, name=obj_current.name)

    new_obj = await crud.analysis.create(obj_in=sch)
    return create_response(data=new_obj)

@router.put("/{id}", response_model=PutResponseBaseSch[AnalysisSch])
async def update(
    id: str,
    sch: AnalysisUpdateSch
):
    """
    Updates a obj by its id
    """
    obj_current = await crud.analysis.get(id=id)
    if not obj_current:
        raise IdNotFoundException(Analysis, id)
    # name = await crud.analysis.get_by_name(name=sch.name)
    # if name:
    #     raise NameExistException(Analysis, sch.name)
    obj_updated = await crud.analysis.update(obj_current=obj_current, obj_new=sch)
    return create_response(data=obj_updated)
