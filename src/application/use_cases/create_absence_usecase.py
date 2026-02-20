

from src.application.dto.absence_dto import CreateAbsenceDTO
from http.client import HTTPException
from src.domain.entities.absence import Absence
from src.infrastructure.logger import logger
from src.domain.repositories.absence_repository import AbsenceRepository
from datetime import datetime

class CreateAbsenceUseCase:
    def __init__(self, repository: AbsenceRepository):
        self.repository = repository

    async def execute(self, dto: CreateAbsenceDTO, user: dict) -> Absence:
            absence = Absence(**dto.dict())

            absence.date_start = datetime.combine(absence.date_start, datetime.min.time())
            absence.date_end = datetime.combine(absence.date_end, datetime.min.time())

            logger.info(f"Usuario {user['preferred_username']} criando ausencia")
            return await self.repository.create(absence)
        
