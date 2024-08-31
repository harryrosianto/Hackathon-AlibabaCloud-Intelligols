from models.bean_quality import BeanQualityBase, BeanQualityFullBase
from util.partial import optional


class BeanQualityCreateSch(BeanQualityBase):
    pass

class BeanQualitySch(BeanQualityFullBase):
    pass

@optional
class BeanQualityUpdateSch(BeanQualityBase):
    pass