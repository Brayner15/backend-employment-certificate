from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, create_pdf_analytics, employment
from app.utils.db import init_db

app = FastAPI()

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Para desarrollo local
        "http://3.22.51.141"       # IP pública en AWS (ajusta según tu caso)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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