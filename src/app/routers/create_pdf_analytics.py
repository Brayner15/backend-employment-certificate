# app/routers/create_pdf_analytics.py
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.utils.db import get_db
from app.services.generate_pdf_service import create_pdf_service
from app.routers.auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class PDFRequest(BaseModel):
    user_id: int

@router.post("/generate_pdf_report")
async def generate_pdf_report(
    request: PDFRequest,
    db: Session = Depends(get_db)
):
    try:
        pdf_content, filename = create_pdf_service(db, request.user_id)
        
        return Response(
            content=pdf_content,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el informe PDF: {str(e)}"
        )