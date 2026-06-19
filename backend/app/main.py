from fastapi import FastAPI

from app.api import upload, events
from app.database import Base, engine
from app.models import Event, Alert

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Cloud Identity Detection API",
    description="API for detecting identity-based attacks from authentication and audit logs.",
    version="0.1.0"
)

app.include_router(upload.router, prefix="/upload",tags= ["Upload"])
app.include_router(events.router, prefix="/events", tags=["Events"])

@app.get("/health")
def health_check():
    return {"status": "ok"}