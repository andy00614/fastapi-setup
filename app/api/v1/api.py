# app/api/v1/api.py
from fastapi import APIRouter
from fastapi.responses import JSONResponse, StreamingResponse
from app.schemas.llm import GenerateRequest
from app.llm import generate_sync, generate_stream

model_router = APIRouter(prefix="/v1", tags=["llm"])

@model_router.post("/generate")
def generate(req: GenerateRequest):
    if req.stream:
        return StreamingResponse(generate_stream(req), media_type="text/event-stream")
    else:
        out = generate_sync(req)
        return JSONResponse(out.model_dump())
