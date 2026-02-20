

from typing import List
from src.application.dto.absence_dto import ListAbsenceDTO
from http.client import HTTPException
from src.domain.entities.absence import Absence
from src.infrastructure.logger import logger
from src.domain.repositories.absence_repository import AbsenceRepository

class ListAbsenceUseCase:
    def __init__(self, repository: AbsenceRepository):
        self.repository = repository

    async def execute(self, dto: ListAbsenceDTO, user: dict) -> List[Absence]:
        try:
            logger.info(f"Usuario {user['preferred_username']} listando ausencias")
            return await self.repository.list_all(page=dto.page, limit=dto.limit)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
