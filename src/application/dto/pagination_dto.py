from pydantic import BaseModel

class PaginationDTO(BaseModel):
    page: int = 1
    limit: int = 20

