from src.infrastructure.logger import logger
import src.infrastructure.logger
from src.infrastructure.security.keycloak_auth import jwt_auth
from fastapi import APIRouter, Depends, HTTPException
from src.application.dto.absence_dto import CreateAbsenceDTO
from src.infrastructure.database.mongo_client import get_absence_repository

router = APIRouter(prefix="/api/v1/absences")

@router.post("/", response_model=Absence)
async def create_absence(
        dto: CreateAbsenceDTO, repo= 
        Depends(get_absence_repository),
        user= Depends(jwt_auth)):
    logger.info(f"Usuario {user['preferred_username']} criando ausencia")
    absence = Absence(**dto.dict())
    return await repo.create(absence)

@router.get("/", response_model=List[Absence])
async def list_absences(
    pagination: PaginationDTO = Depends(),
    repo= Depends(get_absence_repository),
    user= Depends(jwt_auth)):
    
    logger.info(f"Usuário {user['preferred_username']} listando ausências")
    return await repo.list_all(page=pagination.page, limit=pagination.limit)


@router.get("/{absence_id}", response_model=Absence)
async def get_abence(
        absence_id: str,
        repo: Depends(get_absence_repository),
        user = Depends(jwt_auth)):
    absence = await repo.get_by_id(absence_id)
    if not absence:
        raise HTTPException(status_code=404, detail="Ausencia nao encontrada")
    return absence

@route.patch("/{absence_id}", response_model=Absence)
async def update_absence(
    absence_id: str,
    repo = Depends(get_absence_repository),
    user = Depends(jwt_auth)):

    updated = await repo.update(absence_id, dto.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Ausencia nao encontrada")
    logger.info(f"Usuario {user['preferred_username']} atualizou ausencia {absence_id}")
    return updated


# GET /api/v1/absences/employee/{employee_id}
@router.get("/employee/{employee_id}", response_model=List[Absence])
async def absences_by_employee(
    employee_id: str,
    pagination: PaginationDTO = Depends(),
    repo = Depends(get_absence_repository),
    user = Depends(jwt_auth)):
    return await repo.filter_by_employee(employee_id, page=pagination.page, limit=pagination.limit)

# GET /api/v1/absences/status/{status}
@router.get("/status/{status}", response_model=List[Absence])
async def absences_by_status(status: str,
                             pagination: PaginationDTO = Depends(),
                             repo = Depends(get_absence_repository),
                             user = Depends(jwt_auth)):
    return await repo.filter_by_status(status, page=pagination.page, limit=pagination.limit)
