import subprocess

from fastapi import FastAPI

app = FastAPI()


VALIDATION_SCRIPT = "scripts/cleaning_service.py"


@app.post("/cleaning")
def run_validation():
    subprocess.Popen(["python", VALIDATION_SCRIPT])
    return {"status": "Clearning script started running"}
