from models.roast_level import RoastLevelBase, RoastLevelFullBase
from util.partial import optional


class RoastLevelCreateSch(RoastLevelBase):
    pass

class RoastLevelSch(RoastLevelFullBase):
    pass

@optional
class RoastLevelUpdateSch(RoastLevelBase):
    pass