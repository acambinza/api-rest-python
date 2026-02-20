

from src.infrastructure.logger import logger
from http.client import HTTPException
from src.domain.entities.absence import Absence
from src.domain.repositories.absence_repository import AbsenceRepository

class GetAbsenceByEmployeeIdUseCase:
    def __init__(self, repository: AbsenceRepository):
        self.repository = repository

    async def execute(self, employee_id:str, user: dict, page: int = 1, limit: int = 20) -> Absence:
        try:
            logger.info(f"Usuario {user['preferred_username']} buscando ausencia {employee_id}")
            return await self.repository.filter_by_employee(employee_id, page, limit)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
