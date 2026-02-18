from src.infrastructure.security.keycloak_auth import jwt_auth
from sys import prefix
from fastapi import APIRouter, Depends, HTTPException
from src.application.dto.absence_dto import CreateAbsenceDTO
from src.infrastructure.database.mongo_client import get_absence_repository

router = APIRouter(prefix="/api/v1/absences")

@router.post("/", response_model=Absence)
async def create_absence(
        dto: CreateAbsenceDTO, repo= 
        Depends(get_absence_repository),
        user= Depends(jwt_auth)):
    absence = Absence(**dto.dict())
    return await repo.create(absence)

@router.get("/", response_model=list[Absence])
async def list_absences(
    repo= Depends(get_absence_repository),
    user= Depends(jwt_auth)):
    return await repo.list_all()