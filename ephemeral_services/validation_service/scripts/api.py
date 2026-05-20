import subprocess

from fastapi import FastAPI

app = FastAPI()


VALIDATION_SCRIPT = "scripts/validation_service.py"


@app.post("/validation")
def run_validation():
    subprocess.Popen(["python", VALIDATION_SCRIPT])
    return {"status": "Validation script started running"}
