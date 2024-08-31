from pydantic import BaseModel
from models.user import UserBase
from util.partial import optional

class UserRegisterSch(BaseModel):
    username: str
    name: str
    email: str
    password: str
    role_id: str

    class Config:
        hashed_password = None

class UserCreateSch(UserBase):
    pass

class UserSch(UserBase):
    pass

@optional
class UserUpdateSch(UserBase):
    pass