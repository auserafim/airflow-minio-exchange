import httpx
from fastapi import FastAPI, Request

app = FastAPI()

AIRFLOW_URL = "http://airflow:8080/api/v2/dags/Main-Orchestration/dagRuns"


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    print("EVENT RECEIVED")
    print(body)

    payload = {
        "conf": {
            "key": body["Key"],
            "event_time": body["Records"][0]["eventTime"],
            "event_name": body["EventName"],
        }
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(AIRFLOW_URL, json=payload)

    return {
        "status": "ok",
        "airflow_status": response.status_code,
    }


@app.get("/")
def status():
    return {"status": "alive"}
