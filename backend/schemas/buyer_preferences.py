from models.buyer_preferences import BuyerPreferencesBase, BuyerPreferencesFullBase
from util.partial import optional


class BuyerPreferencesCreateSch(BuyerPreferencesBase):
    pass

class BuyerPreferencesSch(BuyerPreferencesFullBase):
    pass

@optional
class BuyerPreferencesUpdateSch(BuyerPreferencesBase):
    pass