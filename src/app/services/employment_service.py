from sqlalchemy.orm import Session
from app.models.employment_model import Employment
from app.schemas.employment_schema import EmploymentCreate

def create_employment(db: Session, employment: EmploymentCreate):
    db_employment = Employment(
        user_id=employment.user_id,
        start_date=employment.start_date,
        contract_type=employment.contract_type,
        salary=employment.salary,
        position=employment.position,
        department=employment.department
    )
    db.add(db_employment)
    db.commit()
    db.refresh(db_employment)
    return db_employment

def info_employment(db: Session, user_id: int):
    return db.query(Employment).filter(Employment.user_id == user_id).first()