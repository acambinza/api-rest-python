from datetime import date 
from pydantic import BaseModel, validator
from typing import Optional

class Absence(BaseModel):
    id: Optional[str ] = None 
    employee_id: str
    reason: str
    date_start: date
    date_end: date

    
    @validator("date_end")
    def end_after_start(cls, v, values):
        start = values.get("date_start")
        if start and v < start:
            raise ValueError("date_end cannot be before date_start")
        return v
    
    def duration_days(self) -> int:
        """ Retorna o numero de dias de ausencias """
        return (self.date_end - self.date_start).days + 1

    def is_vacation(self) -> bool:
        """Verifica se a ausencia e do tipo ferias"""
        return self.reason.lower() == "ferias"

    



    