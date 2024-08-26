from models.user import UserBase, UserFullBase
from util.partial import optional


class UserCreateSch(UserBase):
    pass

class UserSch(UserFullBase):
    pass

@optional
class UserUpdateSch(UserBase):
    pass