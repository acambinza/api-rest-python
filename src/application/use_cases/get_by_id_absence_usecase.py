

from src.infrastructure.logger import logger
from http.client import HTTPException
from src.domain.entities.absence import Absence
from src.domain.repositories.absence_repository import AbsenceRepository

class GetAbsenceByIdUseCase:
    def __init__(self, repository: AbsenceRepository):
        self.repository = repository

    async def execute(self, absence_id:str, user: dict) -> Absence:
        try:
            logger.info(f"Usuario {user['preferred_username']} buscando ausencia {absence_id}")
            return await self.repository.get_by_id(absence_id)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
