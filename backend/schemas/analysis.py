from models.analysis import AnalysisBase, AnalysisFullBase
from util.partial import optional


class AnalysisCreateSch(AnalysisBase):
    pass

class AnalysisSch(AnalysisFullBase):
    pass

@optional
class AnalysisUpdateSch(AnalysisBase):
    pass