from typing import Optional
from abc import ABC, abstractmethod
from typic import List
from src.domain.entities.absence import Absence

class AbsenceRepository(ABC):
    @abstractmethod
    async def create(self, absence: Absence) -> Absence:
        pass

    @abstractmethod
    async def list_all(self, page: int = 1, limit: init = 20) -> List[Absence]:
        pass

    @abstractmethod
    async def get_by_id(self, absence_id: str) -> Optional[Absence]:
        pass

    @abstractmethod
    async def update(self, absence_id: str, data: dict) ->Optional[Absence]:
        pass

    @abstractmethod
    async def delete(self, absence_id: str) -> bool:
        pass

    @abstractmethod
    async def filter_by_employee(self, employee_id: str, page: int = 1, limit: int = 20) -> List[Absence]:
        pass

    @abstractmethod
    async def filter_by_status(self, status: str, page: int = 1, limit: int = 20) -> List[Absence]:
        pass

    
