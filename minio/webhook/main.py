from datetime import UTC, datetime

import httpx
from fastapi import FastAPI, Request

app = FastAPI()

ENDPOINT_URL = "http://airflow:8080"
# dag id in this case is the mainorchestrator
AIRFLOW_URL = f"{ENDPOINT_URL}/api/v2/dags/mainorchestrator/dagRuns"


def get_jwt_token() -> str:
    payload = {"username": "admin", "password": "admin"}
    response = httpx.post(f"{ENDPOINT_URL}/auth/token", json=payload)
    token = response.json()["access_token"]
    return token


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    print("EVENT RECEIVED")

    payload = {
        "logical_date": datetime.now(UTC).isoformat(),
        "conf": {
            "key": body["Key"],
            "event_time": body["Records"][0]["eventTime"],
            "event_name": body["EventName"],
        },
    }
    token = get_jwt_token()

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    async with httpx.AsyncClient() as client:
        response = await client.post(AIRFLOW_URL, json=payload, headers=headers)

    print(f"Airflow Response {response.status_code}")
    print(response.text)
    return {
        "status": "ok",
        "airflow_status": response.status_code,
    }
