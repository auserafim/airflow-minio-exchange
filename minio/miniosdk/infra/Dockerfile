FROM python:3.12-slim

WORKDIR /app

COPY infra/requirements.txt .

RUN pip install -r requirements.txt

CMD ["tail" ,"-f" ,"/dev/null"]
