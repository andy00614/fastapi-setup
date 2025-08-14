import json
import time
from typing import List
import uuid
from app.api.v1.api import  model_router
from fastapi import FastAPI
from app.core.config import settings
from app.schemas.llm import GenerateRequest
from fastapi.responses import JSONResponse, StreamingResponse



app = FastAPI(
    title = settings.PROJECT_NAME,
    version= settings.VERSION
)

app.include_router(model_router)

@app.get("/")
async def root():
    return {"name": settings.PROJECT_NAME, "version": settings.VERSION}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": settings.VERSION}
