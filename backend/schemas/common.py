from enum import Enum, IntEnum


class OrderEnumSch(str, Enum):
    ascendent = "ascendent"
    descendent = "descendent"

class IsActiveEnumSch(str, Enum):
    false = 'false'
    true = 'true'

class GenderEnum(str, Enum):
    female = "female"
    male = "male"
    other = "other"