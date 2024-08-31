
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.crud import CRUDBase
from fastapi_async_sqlalchemy import db

from models.analysis import Analysis
from schemas.analysis import AnalysisCreateSch, AnalysisUpdateSch

class CRUDAnalysis(CRUDBase[Analysis, AnalysisCreateSch, AnalysisUpdateSch]):    
    pass

analysis = CRUDAnalysis(Analysis)
