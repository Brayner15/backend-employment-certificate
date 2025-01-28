from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import os

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:root@db/bd_fastapi")

def get_engine(max_retries=5):
    retry_count = 0
    while retry_count < max_retries:
        try:
            engine = create_engine(
                SQLALCHEMY_DATABASE_URL,
                pool_pre_ping=True,
                pool_recycle=3600,
            )
            # Verificar la conexión
            engine.connect()
            return engine
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                raise Exception(f"No se pudo conectar a la base de datos después de {max_retries} intentos: {str(e)}")
            print(f"Intento {retry_count} de {max_retries} fallido. Reintentando en 5 segundos...")
            time.sleep(5)

engine = get_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            import app.models.user_model
            import app.models.employment_model
            import app.models.generate_pdf_model
            import app.models.profile_user_model
            Base.metadata.create_all(bind=engine)
            print("Base de datos inicializada correctamente")
            db = SessionLocal()
            if db.query(app.models.profile_user_model.ProfileUser).count() == 0:
                db.add_all([
                    app.models.profile_user_model.ProfileUser(id_profile=1, name="Administrador"),
                    app.models.profile_user_model.ProfileUser(id_profile=2, name="Empleado")
                ])
                db.commit()
                print("Registros iniciales insertados en la tabla profile_user")
            
            print("Base de datos inicializada correctamente")
            return
        except Exception as e:
            retry_count += 1
            if retry_count == max_retries:
                raise Exception(f"No se pudo inicializar la base de datos después de {max_retries} intentos: {str(e)}")
            print(f"Intento {retry_count} de {max_retries} fallido. Reintentando en 5 segundos...")
            time.sleep(5)