from fastapi import FastAPI

app = FastAPI(
    title="Cloud Identity Detection API",
    description="API for detecting identity-based attacks from authentication and audit logs.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}