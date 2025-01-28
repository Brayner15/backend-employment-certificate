from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.schemas.employment_schema import EmploymentCreate, Employment
from app.services.employment_service import create_employment

router = APIRouter()

@router.post("/", response_model=Employment)
async def add_employment(employment: EmploymentCreate, db: Session = Depends(get_db)):
    try:
        db_employment = create_employment(db, employment)
        return db_employment
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al agregar la información de empleo: {str(e)}")