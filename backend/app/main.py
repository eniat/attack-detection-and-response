from fastapi import FastAPI

from app.api import upload
from app.database import Base, engine
from app.models import Event

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Identity Detection API",
    description="API for detecting identity-based attacks from authentication and audit logs.",
    version="0.1.0"
)

app.include_router(upload.router, prefix="/upload",tags= ["Upload"])

@app.get("/health")
def health_check():
    return {"status": "ok"}