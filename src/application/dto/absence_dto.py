from pydantic import BaseModel
from datetime import date 

class CreateAbsenceDTO(BaseModel):
    employee_id: str 
    reason: str
    date_start: date
    date_end: date


class ListAbsenceDTO(BaseModel):
    page: int = 1
    limit: int = 20


class UpdateAbsenceDTO(BaseModel):
    reason: str | None = None
    date_start: date | None = None
    date_end: date | None = None
    employee_id: str | None = None
