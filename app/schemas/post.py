from typing import Optional
from pydantic import BaseModel, Field


class PostBase(BaseModel):
    title: str = Field(...,min_length=1,max_length=50)
    content: str = Field(...,min_length=1)

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    content: Optional[str] = Field(None, min_length=1)

class PostOut(PostBase):
    id: int