import subprocess

from fastapi import FastAPI

app = FastAPI()


ANALYTICS_SERVICE = "scripts/analytics_service.py"


@app.post("/analytics")
def run_validation():
    subprocess.Popen(["python", ANALYTICS_SERVICE])
    return {"status": "Analytics script started running"}
