from abc import ABC, abstractmethod
from typic import List
from src.domain.entities.absence import Absence

class AbsenceRepository(ABC):
    @abstractmethod
    async def create(self, absence: Absence) -> Absence:
        pass

    @abstractmethod
    async def list_all(self) -> List[Absence]:
        pass

    