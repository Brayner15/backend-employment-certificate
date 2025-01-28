from pydantic import BaseModel
from typing import Optional

class GeneratePDFRequest(BaseModel):
    user_id: int

class PDFResponse(BaseModel):
    status: str
    data: dict

