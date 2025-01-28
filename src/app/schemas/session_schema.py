from pydantic import BaseModel
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: str

class SessionResponse(BaseModel):
    id: str
    user_id: str
    created_at: datetime
    expires_at: datetime

    class Config:
        orm_mode = True
