from typing import List, Optional
from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str

class GenerateRequest(BaseModel):
    model_name: str
    messages: Optional[List[Message]] = None
    input: Optional[str] = None
    temperature: float = 0.0
    stream: bool = False
    include_raw: bool = False   # 先占位，后面接模型时再用