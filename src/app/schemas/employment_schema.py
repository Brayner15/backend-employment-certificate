from datetime import date
from pydantic import BaseModel

class EmploymentCreate(BaseModel):
    user_id: int
    start_date: date
    contract_type: str
    salary: float
    position: str
    department: str

class Employment(BaseModel):
    id: int
    user_id: int
    start_date: str
    contract_type: str
    salary: float
    position: str
    department: str

    class Config:
        orm_mode = True