from app.models.generate_pdf_model import CreatePDF
import json

def create_pdf_service(data):

    try:
        CreatePDF.create_pdf_model(data)

        return 'ok'
    except Exception as e:
        print("error d", e)
        return 'ERROR'