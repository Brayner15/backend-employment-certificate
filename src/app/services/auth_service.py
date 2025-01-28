from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.session_model import Session as DBSession
from datetime import datetime, timedelta
from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserAuth
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        identification_number=user.identification_number,
        id_profile=user.id_profile
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_session(db: Session, user: User) -> str:
    # Limpiar sesiones antiguas del usuario
    clean_expired_sessions(db, user.id)
    
    # Crear nueva sesión
    session_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=1)
    
    db_session = DBSession(
        id=session_id,
        user_id=user.id,
        expires_at=expires_at
    )
    
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    
    return session_id

def validate_session(db: Session, session_id: str) -> User:
    session = (
        db.query(DBSession)
        .filter(DBSession.id == session_id)
        .filter(DBSession.expires_at > datetime.utcnow())
        .first()
    )
    
    if not session:
        return None
        
    return session.user

def delete_session(db: Session, session_id: str) -> bool:
    result = db.query(DBSession).filter(DBSession.id == session_id).delete()
    db.commit()
    return result > 0

def clean_expired_sessions(db: Session, user_id: str):
    db.query(DBSession).filter(
        DBSession.user_id == user_id,
        DBSession.expires_at <= datetime.utcnow()
    ).delete()
    db.commit()

def logout_user(db: Session, session_id: str):
    if delete_session(db, session_id):
        return {"message": "Logout successful"}
    return {"message": "No session found"}