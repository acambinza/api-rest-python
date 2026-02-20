from src.application.use_cases.get_by_employee_id_absence_usecase import GetAbsenceByEmployeeIdUseCase
from src.application.dto.absence_dto import UpdateAbsenceDTO
from src.application.use_cases.update_absence_usecase import UpdateAbsenceUseCase
from src.application.use_cases.get_by_id_absence_usecase import GetAbsenceByIdUseCase
from src.application.use_cases.list_absence_usecase import ListAbsenceUseCase
from src.application.use_cases.create_absence_usecase import CreateAbsenceUseCase
from typing import List
from src.infrastructure.logger import logger
from src.infrastructure.security.keycloak_auth import jwt_auth
from fastapi import APIRouter, Depends, HTTPException
from src.application.dto.absence_dto import CreateAbsenceDTO
from src.infrastructure.database.mongo_client import get_absence_repository
from src.domain.entities.absence import Absence
from src.application.dto.pagination_dto import PaginationDTO


router = APIRouter(prefix="/api/v1/absences")

@router.post("/", response_model=Absence,
responses={
        400: {"description": "Request inválido, dados incorretos ou datas inconsistentes"},
        401: {"description": "Não autorizado"},
        404: {"description": "Recurso não encontrado"}
    })
async def create_absence(
    dto: CreateAbsenceDTO,
    repo=Depends(get_absence_repository),
    user=Depends(jwt_auth)
):
    try:
        use_case = CreateAbsenceUseCase(repository=repo)
        absence = await use_case.execute(dto, user)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return absence


@router.get("/", response_model=List[Absence])
async def list_absences(
    pagination: PaginationDTO = Depends(),
    repo= Depends(get_absence_repository),
    user= Depends(jwt_auth)):
    
    use_case = ListAbsenceUseCase(repository=repo)
    return await use_case.execute(pagination, user)


@router.get("/{absence_id}", response_model=Absence)
async def get_abence(
        absence_id: str,
        repo = Depends(get_absence_repository),
        user = Depends(jwt_auth)):

    use_case = GetAbsenceByIdUseCase(repository=repo)
    absence = await use_case.execute(absence_id, user)
    if not absence:
        raise HTTPException(status_code=404, detail="Ausencia não encontrada")
    return absence

@router.put("/{absence_id}", response_model=Absence)
async def update_absence(
    absence_id: str,
    dto: UpdateAbsenceDTO,
    repo = Depends(get_absence_repository),
    user = Depends(jwt_auth)):

    try:
        use_case = UpdateAbsenceUseCase(repository=repo)
        absence = await use_case.execute(absence_id, dto, user)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))

    return absence


# GET /api/v1/absences/employee/{employee_id}
@router.get("/employee/{employee_id}", response_model=List[Absence])
async def absences_by_employee(
    employee_id: str,
    pagination: PaginationDTO = Depends(),
    repo = Depends(get_absence_repository),
    user = Depends(jwt_auth)):

    try:
        use_case = GetAbsenceByEmployeeIdUseCase(repository=repo)
        return await use_case.execute(employee_id, user, page=pagination.page, limit=pagination.limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
