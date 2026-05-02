from datetime import UTC, datetime

from fastapi import FastAPI
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    timestamp: str


app = FastAPI(
    title="Task Priority API",
    version="0.1.0",
)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
    }
