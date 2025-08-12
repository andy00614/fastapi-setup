from app.api.v1.api import api_router
from fastapi import FastAPI
from app.core.config import settings


app = FastAPI(
    title = settings.PROJECT_NAME,
    version= settings.VERSION
)

app.include_router(api_router,prefix="/api/v1")

@app.get("/")
async def root():
    return {"name": settings.PROJECT_NAME, "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}