# app/schemas/llm.py
from typing import Optional, List, Literal, Dict, Any
from pydantic import BaseModel

Role = Literal["system", "user", "assistant"]

class Message(BaseModel):
    role: Role
    content: str

class GenerateRequest(BaseModel):
    model_name: str
    messages: Optional[List[Message]] = None
    input: Optional[str] = None        # 单轮便捷输入
    temperature: float = 0.0
    stream: bool = False
    include_raw: bool = False          # 由你控制是否透传供应商原始响应

class Usage(BaseModel):
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    reasoning_tokens: Optional[int] = None

class Choice(BaseModel):
    index: int
    content: str
    finish_reason: str = "stop"

class UnifiedResponse(BaseModel):
    id: str
    created: int
    provider: str
    model: str
    choices: List[Choice]
    usage: Usage
    observability: Dict[str, Any] | None = None
    raw: Dict[str, Any] | None = None
