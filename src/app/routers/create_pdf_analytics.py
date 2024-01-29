from fastapi.responses import JSONResponse
from app.services.generate_pdf_service import create_pdf_service

from fastapi import APIRouter, FastAPI, Form, Body

import fitz
from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.post("/generate_pdf_report")
async def generate_pdf_report(data: dict):
    try:

        status = create_pdf_service(data)
        response = {
            "status": status,
            "data": {
                'msg': 'OK' if True else 'ERROR'
            }
        }
        return JSONResponse(content=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el informe PDF: {str(e)}")
