from models.disease_management import DiseaseManagementBase, DiseaseManagementFullBase
from util.partial import optional


class DiseaseManagementCreateSch(DiseaseManagementBase):
    pass

class DiseaseManagementSch(DiseaseManagementFullBase):
    pass

@optional
class DiseaseManagementUpdateSch(DiseaseManagementBase):
    pass