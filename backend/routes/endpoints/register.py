from fastapi import APIRouter, status

import crud
from schemas.response import PostResponseBaseSch, create_response
from schemas.user import UserRegisterSch, UserSch


router = APIRouter()

@router.post(
    "",
    response_model=PostResponseBaseSch[UserSch],
    status_code=status.HTTP_201_CREATED,
)
async def create(
    sch: UserRegisterSch,
):
    """
    Creates a new obj
    """
    # nanti tambahin cek kalo user exist gmn
    new_obj = await crud.user.create_with_role(obj_in=sch)
    return create_response(data=new_obj)