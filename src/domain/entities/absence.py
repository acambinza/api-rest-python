from datetime import date 
from pydantic import BaseModel

class Absence(BaseModel):
    id: str | None = None 
    employee_id: str
    reason: str
    date_start: date
    date_end: date


    