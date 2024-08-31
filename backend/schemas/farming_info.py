from models.farming_info import FarmingInfoBase, FarmingInfoFullBase
from util.partial import optional


class FarmingInfoCreateSch(FarmingInfoBase):
    pass

class FarmingInfoSch(FarmingInfoFullBase):
    pass

@optional
class FarmingInfoUpdateSch(FarmingInfoBase):
    pass