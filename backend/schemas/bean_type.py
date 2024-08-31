from models.bean_type import BeanTypeBase, BeanTypeFullBase
from util.partial import optional


class BeanTypeCreateSch(BeanTypeBase):
    pass

class BeanTypeSch(BeanTypeFullBase):
    pass

@optional
class BeanTypeUpdateSch(BeanTypeBase):
    pass