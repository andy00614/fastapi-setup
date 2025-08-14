# app/llm.py
import time, uuid, json
from typing import List, Dict, Any, Iterable, Tuple
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

from app.schemas.llm import (
    GenerateRequest, UnifiedResponse, Choice, Usage, Message
)

load_dotenv()

# —— 1) 模型别名与解析（先只放 OpenAI；Gemini 下一步加）——
ALIASES: Dict[str, Tuple[str, str]] = {
    "gpt-4o-mini": ("openai", "gpt-4o-mini"),
    "gpt-4o":      ("openai", "gpt-4o"),
    # Google (NEW)
    "gemini-flash": ("google", "gemini-1.5-flash"),
    "gemini-pro":   ("google", "gemini-1.5-pro"),
}
def resolve_model(name: str) -> tuple[str, str]:
    if name in ALIASES: return ALIASES[name]
    if "/" in name: return tuple(name.split("/", 1))  # 支持 "openai/gpt-4o-mini"
    raise ValueError(f"未知模型名：{name}")

# —— 2) 输入归一（messages 或 input → messages[dict]）——
def normalize_messages(req: GenerateRequest) -> List[dict]:
    if req.messages and len(req.messages) > 0:
        return [m.model_dump() for m in req.messages]
    if req.input:
        return [{"role": "user", "content": req.input}]
    raise ValueError("messages 或 input 至少提供一个")

def to_lc_messages(messages: List[dict]):
    out = []
    for m in messages:
        if m["role"] == "system":
            out.append(SystemMessage(content=m["content"]))
        else:
            out.append(HumanMessage(content=m["content"]))
    return out

# —— 3) OpenAI 同步调用，返回统一字段 —— 
def _run_openai_sync(real_model: str, messages: List[dict], temperature: float, include_raw: bool) -> Dict[str, Any]:
    llm = ChatOpenAI(model=real_model, temperature=temperature)
    resp = llm.invoke(to_lc_messages(messages))
    raw = dict(resp)
    usage = getattr(resp, "usage_metadata", {}) or {}
    return {
        "provider": "openai",
        "model": real_model,
        "text": getattr(resp, "content", ""),
        "finish_reason": getattr(resp, "finish_reason", "stop"),
        "usage": {
            "prompt_tokens": usage.get("input_tokens", 0),
            "completion_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
        },
        "raw": raw
    }

# —— NEW 3) Gemini 同步调用，返回统一字段 ——
def _run_gemini_sync(real_model: str, messages: List[dict], temperature: float, include_raw: bool) -> Dict[str, Any]:
    print(real_model)
    llm = ChatGoogleGenerativeAI(
        model=real_model,
        temperature=temperature,
        # 如需更严格安全：safety_settings={...}
    )
    resp = llm.invoke(to_lc_messages(messages))
    
    usage = getattr(resp, "usage_metadata", {}) or {}
    # Gemini 的 usage 字段名与 OpenAI 略有不同，这里做兼容兜底：
    pt = usage.get("prompt_token_count") or usage.get("input_tokens") or 0
    ct = usage.get("candidates_token_count") or usage.get("output_tokens") or 0
    tt = usage.get("total_token_count") or usage.get("total_tokens") or (pt + ct)
    rt = usage.get("thoughts_token_count") or usage.get("reasoning_tokens")
    raw = dict(resp)
    return {
        "provider": "google",
        "model": real_model,
        "text": getattr(resp, "content", ""),
        "finish_reason": getattr(resp, "finish_reason", "stop"),
        "usage": {
            "prompt_tokens": pt,
            "completion_tokens": ct,
            "total_tokens": tt,
            "reasoning_tokens": rt,
        },
        "raw": raw
    }


# —— 4) 对外：同步统一响应 —— 
def generate_sync(req: GenerateRequest) -> UnifiedResponse:
    messages = normalize_messages(req)
    provider, real = resolve_model(req.model_name)

    req_id = "req_" + uuid.uuid4().hex[:16]
    created = int(time.time())
    t0 = time.perf_counter()

    if provider == "openai":  # CHANGE
        result = _run_openai_sync(real, messages, req.temperature, req.include_raw)
    elif provider == "google":  # NEW
        result = _run_gemini_sync(real, messages, req.temperature, req.include_raw)
    else:
        raise ValueError(f"暂不支持的 provider: {provider}")

    latency = int((time.perf_counter() - t0) * 1000)

    usage = Usage(**result["usage"])
    return UnifiedResponse(
        id=req_id,
        created=created,
        provider=result["provider"],
        model=result["model"],
        choices=[Choice(index=0, content=result["text"], finish_reason=result["finish_reason"])],
        usage=usage,
        observability={"latency_ms": latency, "cost_usd": 0.0, "estimated": True},
        raw=(result["raw"] if req.include_raw else None),
    )


# —— 5) 流式（SSE）：产出统一事件 —— 
def sse_event(event: str, data: dict) -> str:
    return f"event: {event}\n" + "data: " + json.dumps(data, ensure_ascii=False) + "\n\n"

def generate_stream(req: GenerateRequest) -> Iterable[str]:
    messages = normalize_messages(req)
    provider, real = resolve_model(req.model_name)

    if provider == "openai":
        llm = ChatOpenAI(model=real, temperature=req.temperature)
        meta = {"id":"req_"+uuid.uuid4().hex[:16], "created":int(time.time()), "provider":"openai", "model":real}
        yield sse_event("meta", meta)
        for chunk in llm.stream(to_lc_messages(messages)):
            part = getattr(chunk, "content", None)
            text = "".join(str(p) for p in part) if isinstance(part, list) else (part if isinstance(part, str) else "")
            if text:
                yield sse_event("delta", {"index": 0, "delta": text})
        yield sse_event("done", {"usage":{"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}, "latency_ms":0})
        return

    if provider == "google":  # NEW
        llm = ChatGoogleGenerativeAI(model=real, temperature=req.temperature)
        meta = {"id":"req_"+uuid.uuid4().hex[:16], "created":int(time.time()), "provider":"google", "model":real}
        yield sse_event("meta", meta)
        for chunk in llm.stream(to_lc_messages(messages)):
            part = getattr(chunk, "content", None)
            text = "".join(str(p) for p in part) if isinstance(part, list) else (part if isinstance(part, str) else "")
            if text:
                yield sse_event("delta", {"index": 0, "delta": text})
        yield sse_event("done", {"usage":{"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}, "latency_ms":0})
        return

    # 其他 provider（暂不支持）
    yield sse_event("meta", {"id":"req_stub","created":int(time.time()),"provider":provider,"model":real})
    yield sse_event("delta", {"index":0, "delta":"该 provider 的流式将在后续接入"})
    yield sse_event("done", {"usage":{"prompt_tokens":0,"completion_tokens":0,"total_tokens":0}, "latency_ms":0})
