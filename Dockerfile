# Usa una imagen base de Python
FROM python:3.11.3-bullseye

# Establece el directorio de trabajo en /src
WORKDIR /code

# Copia el archivo requirements.txt al directorio de trabajo
COPY ./src/requirements.txt /code/requirements.txt

# Instala las dependencias
RUN pip install uvicorn
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copia el contenido del directorio app en el directorio de trabajo
COPY ./src/app /code/app

# Configura el comando por defecto para ejecutar la aplicación con uvicorn
CMD ["uvicorn", "app.main:app", "--reload","--host", "0.0.0.0", "--port", "8500"]