
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.disease_management import DiseaseManagement
from schemas.disease_management import DiseaseManagementCreateSch, DiseaseManagementUpdateSch

class CRUDDiseaseManagement(CRUDBase[DiseaseManagement, DiseaseManagementCreateSch, DiseaseManagementUpdateSch]):    
    pass

disease_management = CRUDDiseaseManagement(DiseaseManagement)
