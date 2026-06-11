from fastapi import FastAPI

from app.database import Base, engine
from app.models import Event

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Identity Detection API",
    description="API for detecting identity-based attacks from authentication and audit logs.",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}