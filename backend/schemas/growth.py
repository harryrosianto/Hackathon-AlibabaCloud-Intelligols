from models.growth import GrowthBase, GrowthFullBase
from util.partial import optional


class GrowthCreateSch(GrowthBase):
    pass

class GrowthSch(GrowthFullBase):
    pass

@optional
class GrowthUpdateSch(GrowthBase):
    pass