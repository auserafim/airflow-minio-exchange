FROM python:3.12-slim

WORKDIR /app

COPY infra/requirements.txt .
COPY scripts/ app/scripts/

RUN pip install -r requirements.txt
EXPOSE 8003
CMD ["uvicorn", "scripts.api:app", "--host", "0.0.0.0", "--port", "8003"]
