from enum import Enum, IntEnum


class OrderEnumSch(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"

class IsActiveEnumSch(str, Enum):
    false = 'false'
    true = 'true'

class UserRoleEnum(IntEnum):
    ADMIN = 1
    FARMER = 2
    BUYER = 3