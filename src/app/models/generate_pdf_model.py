import io
import json

from fastapi import HTTPException
from fastapi.responses import StreamingResponse

import fitz
class CreatePDF:
    def create_pdf_model(data):
        try:
            
            # Aquí puedes agregar lógica para procesar los datos y generar el informe PDF
            pdf_document = fitz.open()
            page = pdf_document.new_page(width=500, height=500)
            page.insert_text((100, 100), f"Datos recibidos: {data}", fontname="helv", fontsize=12)
            pdf_content = pdf_document.write()
            pdf_document.close()

            # Retorna el contenido del PDF como una StreamingResponse
            return StreamingResponse(io.BytesIO(pdf_content), media_type="application/pdf", headers={"Content-Disposition": "inline; filename=informe.pdf"})

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al generar el informe PDF: {str(e)}") 
