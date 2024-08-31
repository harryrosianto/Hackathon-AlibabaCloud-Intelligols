from models.marketplace import MarketplaceBase, MarketplaceFullBase
from util.partial import optional


class MarketplaceCreateSch(MarketplaceBase):
    pass

class MarketplaceSch(MarketplaceFullBase):
    pass

@optional
class MarketplaceUpdateSch(MarketplaceBase):
    pass