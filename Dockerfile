FROM python:3.9-slim

WORKDIR /code

COPY src/requirements.txt /code/

RUN apt-get update && apt-get install -y \
    mariadb-client \
    libmariadb-dev \
    gcc \
    python3-dev \
    musl-dev

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY src/ /code/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

