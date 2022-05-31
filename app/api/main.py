from fastapi import FastAPI

from app.api.v1 import api_router as v1_router
from app.core.config import settings

app = FastAPI(
    title="Tasks API", openapi_url=f"{settings.API_V1_STR}/openapi.json"
)


@app.get("/")
def root():
    """not async"""
    return "ok"


app.include_router(v1_router, prefix=settings.API_V1_STR)
