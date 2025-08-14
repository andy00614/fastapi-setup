import json
import time
from typing import List
import uuid
from app.api.v1.api import api_router
from fastapi import FastAPI
from app.core.config import settings
from app.schemas.llm import GenerateRequest
from fastapi.responses import JSONResponse, StreamingResponse



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


def normalize_messages(req: GenerateRequest) -> List[dict]:
    print(req.messages)
    if req.messages:
        return [m.model_dump() for m in req.messages]
    if req.input:
        return [{"role": "user", "content": req.input}]
    raise ValueError("messages 或 input 至少提供一个")

def sse_event(event: str, data: dict) -> str:
    return f"event: {event}\n" + "data: " + json.dumps(data, ensure_ascii=False) + "\n\n"

@app.post("/v1/generate")
def generate(req: GenerateRequest):
    msgs = normalize_messages(req)
    print(msgs)
    # 现在还没接模型：先做占位，证明“统一输入/输出”无误
    if req.stream:
        def gen():
            meta = {
                "id": "req_" + uuid.uuid4().hex[:8],
                "created": int(time.time()),
                "provider": "stub",
                "model": req.model_name,
            }
            yield sse_event("meta", meta)
            # 把用户输入当成流式增量演示（占位）
            text = msgs[-1]["content"]
            for piece in ["占位：", text[:10], text[10:]]:
                yield sse_event("delta", {"index": 0, "delta": piece})
            yield sse_event("done", {
                "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
                "latency_ms": 1
            })
        return StreamingResponse(gen(), media_type="text/event-stream")

    # 同步占位响应（统一外形）
    resp = {
        "id": "req_" + uuid.uuid4().hex[:8],
        "created": int(time.time()),
        "provider": "stub",
        "model": req.model_name,
        "choices": [{"index": 0, "content": f"占位响应：{msgs[-1]['content']}", "finish_reason": "stop"}],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "observability": {"latency_ms": 1, "cost_usd": 0.0, "estimated": True},
        "raw": None
    }
    return JSONResponse(resp)