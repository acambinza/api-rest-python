from pydantic import BaseModel
from datetime import date 

class CreateAbsenceDTO(BaseModel):
    emplotee_id: str 
    reason: str
    date_start: date
    date_end: date


