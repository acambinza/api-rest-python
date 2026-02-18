from motor.motor_asyncio import AsyncIOMotorClient
from src.domain.entities.absence import Absence
from src.domain.repositories.absence_repository import AbsenceRepository
from typing import List, Optional

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
    
    async def get_by_id(self, absence_id, str) -> Optional[Absence]:
        try:
            document = await self.collection.find_one({"_id": ObjectId(absence_id)})
        
        except Exception:
            return None
        
        if not document:
            return None
        
        document["id"] = str(document["_id"])
        return Absence(**document)
    
    async def update(self, absence_id: str, data: dict) -> Absence | None:
        result = await self.collection.update_one(
            {"_id": absence_id},
            {"$set": data}
        )
        if result.modified_count:
            doc = await self.collection.find_one({"_id": absence_id})
            doc["id"] = str(doc["_id"])
            return Absence(**doc)
        return None
    
    async def delete(self, absence_id: str) -> bool:
        result = await self.collection.delete_one({"_id":absence_id})
        return result.deleted_count > 0

    async def filter_by_employee(self, employee_id: str, page: int = 1, limit: int = 20) -> List[Absence]:
        skip = (page - 1) * limit
        cursor = self.collection.find(
            {"employee_id":employee_id}).skip(skip).limit(limit)

        results = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            results.append(Absence(**document))
        return results
    
    async def filter_by_status(self, status: str, page: int = 1, limit: int = 20) -> List[Absence]:
        skip = (page - 1) * limit
        cursor = self.collection.find({"status": status}).skip(skip).limit(limit)
        results = []
        async for document in cursor:
            document["id"] = str(document["_id"])
            results.append(Absence(**document))
        return results



def get_absence_repository():
    return MongoAbsenceRepository()
        
    