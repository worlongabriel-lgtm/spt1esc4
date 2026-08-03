from dotenv import load_dotenv
load_dotenv()

from datetime import UTC, datetime

from fastapi import FastAPI
from pydantic import BaseModel

from app.api.task_routes import router as task_router


class HealthResponse(BaseModel):
    status: str
    timestamp: str


app = FastAPI(
    title="Task Priority API",
    version="0.1.0",
)
app.include_router(task_router)


@app.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat(),
    }
