from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, create_pdf_analytics, employment
from app.utils.db import init_db

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL del frontend
    allow_credentials=True,  # Importante para las cookies
    allow_methods=["*"],    # Permite todos los métodos HTTP
    allow_headers=["*"],    # Permite todas las cabeceras
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(create_pdf_analytics.router, prefix="/pdf", tags=["pdf"])
app.include_router(employment.router, prefix="/employment", tags=["employment"])

@app.get("/", tags=['Home'])
async def get_status():
    return {"status": "running"}