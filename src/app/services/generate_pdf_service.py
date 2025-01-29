# app/services/generate_pdf_service.py
from sqlalchemy.orm import Session
from app.models.user_model import User
from app.models.employment_model import Employment
import fitz  # PyMuPDF
from fastapi import HTTPException
from datetime import datetime
from io import BytesIO

def format_currency(amount: float) -> str:
    return f"${amount:,.0f} (PESOS COLOMBIANOS)"

def format_date(date_obj: datetime) -> str:
    months = {
        1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
        5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
        9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"
    }
    return f"{date_obj.day} de {months[date_obj.month]} de {date_obj.year}"

def create_pdf_service(db: Session, user_id: int) -> tuple[bytes, str]:
    try:
        # Consulta los datos del usuario
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Consulta los datos de empleo del usuario
        employment = db.query(Employment).filter(Employment.user_id == user_id).first()
        if not employment:
            raise HTTPException(status_code=404, detail="Datos de empleo no encontrados")

        # Crear el PDF en memoria
        pdf_document = fitz.open()
        page = pdf_document.new_page()

        # Formato de fecha actual
        current_date = format_date(datetime.now())
        start_date = format_date(employment.start_date)
        
        # Crear el contenido del certificado
        text = f"""




        Logo de la empresa
        Nombre de la empresa
        Dirección de la empresa


        


                                CERTIFICADO LABORAL




        Certifica que:

        {user.first_name} {user.last_name}, identificado con Cédula de ciudadanía 
        Nro. {user.identification_number}, labora en la empresa desde el: {start_date} 
        a la fecha, como {employment.position} en el departamento de {employment.department} 
        con un contrato a término {employment.contract_type} y con un salario básico 
        de {format_currency(employment.salary)}.




        Este certificado se expide el {current_date}




        Cordialmente,





        _____________________
        Recursos Humanos
        """

        # Agregar el texto al PDF con formato
        page.insert_text(
            (80, 72),  # Posición inicial
            text,
            fontname="helv",  # Fuente
            fontsize=12,  # Tamaño de fuente
            color=(0, 0, 0)  # Color negro
        )

        # Generar nombre para el PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"certificado_{user_id}_{timestamp}.pdf"

        # Guardar el PDF en un buffer de memoria
        pdf_bytes = BytesIO()
        pdf_document.save(pdf_bytes)
        pdf_document.close()
        
        # Obtener los bytes del PDF
        pdf_content = pdf_bytes.getvalue()
        return pdf_content, pdf_filename

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar el PDF: {str(e)}"
        )