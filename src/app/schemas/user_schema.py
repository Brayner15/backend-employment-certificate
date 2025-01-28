from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class UserCreate(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    identification_number: str
    id_profile: int

class User(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    identification_number: str

    class Config:
        from_attributes = True

class UserAuth(BaseModel):
    username: str
    password: str

class EmploymentCreateInput(BaseModel):
    start_date: date
    contract_type: str
    salary: float
    position: str
    department: str

class UserEmploymentCreate(BaseModel):
    user: UserCreate
    employment: EmploymentCreateInput

class EmploymentResponse(BaseModel):
    start_date: date
    contract_type: str
    salary: float
    position: str
    department: str

class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    identification_number: str
    id_profile: int
    employment: Optional[EmploymentResponse] = None

    model_config = ConfigDict(from_attributes=True)