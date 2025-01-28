from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.orm import Session
from app.schemas.employment_schema import EmploymentCreate
from app.schemas.user_schema import UserCreate, User, UserAuth, UserEmploymentCreate, UserResponse
from app.models.user_model import User as UserModel
from app.models.employment_model import Employment
from app.services.auth_service import (
    create_user, 
    authenticate_user, 
    create_session,
    validate_session,
    delete_session
)
from app.services.employment_service import info_employment, create_employment
from app.utils.db import get_db

router = APIRouter()

def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    session_id = request.cookies.get("session_id")
    if not session_id:
        raise HTTPException(status_code=401, detail="No session found")
    
    user = validate_session(db, session_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    return user

@router.post("/register", response_model=User)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return db_user

@router.post("/login")
def login(
    user: UserAuth, 
    response: Response, 
    db: Session = Depends(get_db)
):
    db_user = authenticate_user(db, user.username, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    session_id = create_session(db, db_user)
    employment_data = info_employment(db, db_user.id)
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=16400,  # 24 horas
        secure=True,    # Solo HTTPS
        samesite="lax"  # Protección CSRF
    )
    employment_info = {}
    if employment_data:
        employment_info = {
            "start_date": employment_data.start_date.strftime("%Y-%m-%d"),
            "contract_type": employment_data.contract_type,
            "salary": employment_data.salary,
            "position": employment_data.position,
            "department": employment_data.department,
            "identification_number": db_user.identification_number
        }

    return {
        "message": "Login successful",
        "user": {
            "id_user": db_user.id,
            "first_name": db_user.first_name,
            "last_name": db_user.last_name,
            "profile": db_user.id_profile,
        },
        "employment":employment_info
    }

@router.post("/logout")
def logout(
    response: Response,
    request: Request,
    db: Session = Depends(get_db)
):
    session_id = request.cookies.get("session_id")
    if session_id:
        delete_session(db, session_id)
        response.delete_cookie(key="session_id")
        return {"message": "Logout successful"}
    return {"message": "No session found"}

# Ejemplo de ruta protegida
@router.get("/info", response_model=User)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user

@router.get("/users")
async def get_users(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.id_profile != 1:
        raise HTTPException(status_code=403, detail="No tiene permisos")
    
    # Consulta los usuarios con sus empleos
    users = db.query(UserModel).filter(UserModel.id != current_user.id).all()
    
    # Procesar los resultados
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "identification_number": user.identification_number,
            "id_profile": user.id_profile,
            "employment": None
        }
        
        # Si el usuario tiene empleo, agregarlo
        if user.employment:  # Asumiendo que tienes la relación definida en el modelo
            employment = user.employment[0] if isinstance(user.employment, list) else user.employment
            user_data["employment"] = {
                "start_date": employment.start_date,
                "contract_type": employment.contract_type,
                "salary": employment.salary,
                "position": employment.position,
                "department": employment.department
            }
        
        user_list.append(UserResponse.model_validate(user_data))
    
    return user_list

@router.post("/users/register")
async def register_user_with_employment(
    data: UserEmploymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id_profile != 1:
        raise HTTPException(
            status_code=403,
            detail="No tiene permisos para registrar usuarios"
        )
    
    try:
        existing_user = db.query(UserModel).filter(UserModel.username == data.user.username).first()
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="El correo electrónico ya está registrado"
            )
        db_user = create_user(db, data.user)
        
        employment_data = data.employment.model_dump()
        employment_data['user_id'] = db_user.id
        
        employment_create = EmploymentCreate(**employment_data)
        db_employment = create_employment(db, employment_create)
        
        return {
            "message": "Usuario registrado exitosamente",
            "user": db_user,
            "employment": db_employment
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error al registrar usuario: {str(e)}"
        )

@router.patch("/users/{user_id}")
async def update_user_partial(
    user_id: int,
    data: dict,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.id_profile != 1:
        raise HTTPException(status_code=403, detail="No tiene permisos")

    try:
        db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        if 'employment' in data:
            db_employment = db.query(Employment).filter(Employment.user_id == user_id).first()
            if db_employment:
                try:
                    for key, value in data['employment'].items():
                        if value:
                            if key == 'salary' and (value > 2147483647 or value < 0):
                                raise HTTPException(
                                    status_code=400, 
                                    detail="El salario está fuera del rango permitido"
                                )
                            setattr(db_employment, key, value)
                except ValueError:
                    raise HTTPException(
                        status_code=400,
                        detail="Valor inválido para uno de los campos"
                    )

        if 'user' in data:
            try:
                for key, value in data['user'].items():
                    if value:
                        setattr(db_user, key, value)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail="Valor inválido para uno de los campos del usuario"
                )

        db.commit()
        return {"message": "Usuario actualizado exitosamente"}

    except HTTPException as e:
        raise e
    except Exception as e:
        db.rollback()
        # Log del error real para debugging
        print(f"Error interno: {str(e)}")
        # Mensaje genérico para el usuario
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el usuario. Por favor, verifique los datos ingresados."
        )


@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    if current_user.id_profile != 1:
        raise HTTPException(status_code=403, detail="No tiene permisos")
    

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    try:
        # Eliminar el usuario y sus datos de empleo (cascada)
        db.delete(user)
        db.commit()
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))