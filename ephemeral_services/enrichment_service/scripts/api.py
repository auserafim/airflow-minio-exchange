import subprocess

from fastapi import FastAPI

app = FastAPI()


ENRICHMENT_SERVICE = "scripts/enrichment_service.py"


@app.post("/enrichment")
def run_validation():
    subprocess.Popen(["python", ENRICHMENT_SERVICE])
    return {"status": "Enrichment script started running"}
