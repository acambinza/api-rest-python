from pydantic import BaseModel
from datetime import date 

class CreateAbsenceDTO(BaseModel):
    emplotee_id: str 
    reason: str
    date_start: date
    date_end: date


class UpdateAbsenceDTO(BaseModel):
    rease: str | None = None
    date_start: date | None = None
    date_end: date | None = None
    status: str | None = None


