FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY docker_etl.py /app/docker_etl.py

CMD ["python", "docker_etl.py"]