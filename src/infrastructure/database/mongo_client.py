from motor.motor_asyncio import AsyncIOMotorClient
from src.domain.entities.absence import Absence
from src.domain.repositories.absence_repository import AbsenceRepository
from typing import List 
import os

MONGO_URI = os.getenv("MONGO_URI","mongodb://mongodb:27017")
DB_NAME = os.getenv("DB_NAME", "company_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

class MongoAbsenceRepository(AbsenceRepository):
    def __init__(self):
        self.collection = db["absences"]

    async def create(self, absence: Absence) -> Absence:
        result = await self.collection.insert_one(absence.dict())
        absence.id = str(result.inserted.id)
        return absence

    async def list_all(self) -> List[Absence]:
        cursor = self.collection.find()
        results = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            results.append(Absence(**document))
        return results


def get_absence_repository():
    return MongoAbsenceRepository()
        
    