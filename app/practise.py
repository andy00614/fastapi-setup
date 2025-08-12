from pydantic import BaseModel, Field
from typing import Optional

# ---- 定义三个 Pydantic 模型（像 TS 的 interface + zod 校验器）----
class PostCreate(BaseModel):
    title: str
    content: str

class PostUpdate(BaseModel):
    # 默认 None，表示“可选字段”
    title: Optional[str] = None
    content: Optional[str] = None

class PostOut(BaseModel):
    id: int
    title: str
    content: str

# ---- 1) 创建时：把请求模型转字典，再解包到响应模型 ----
create_payload = PostCreate(title="Hello", content="FastAPI rocks")
print("1) create_payload.model_dump() ->", create_payload.model_dump())
post = PostOut(id=1, **create_payload.model_dump())  # **dict ≈ JS 的 {...obj}
print("   New PostOut ->", post.model_dump())

# ---- 2) 更新时：只输出“用户实际传入”的字段 ----
empty_update = PostUpdate()               # 没传任何字段
print("\n2) empty_update.model_dump() ->", empty_update.model_dump())  # 默认会带上 None
print("   empty_update.model_dump(exclude_unset=True) ->", empty_update.model_dump(exclude_unset=True))  # {}

title_only = PostUpdate(title="New Title")  # 只改 title
print("   title_only.model_dump(exclude_unset=True) ->", title_only.model_dump(exclude_unset=True))      # {'title': 'New Title'}

# ---- 3) 模拟仓储的“部分更新”逻辑 ----
current = post.model_dump()  # 先把旧对象转成 dict
patch = title_only.model_dump(exclude_unset=True)  # 只拿到用户提供的字段
current.update(patch)  # 像 JS 的 Object.assign(current, patch)
updated = PostOut(**current)  # 重新构造一个合法的 PostOut
print("\n3) updated PostOut ->", updated.model_dump())

# ---- 4) 其他常用选项展示 ----
class WithAlias(BaseModel):
    title: str = Field(..., alias="post_title")
    content: Optional[str] = None

w = WithAlias(post_title="Alias Demo")
print("\n4) alias off  ->", w.model_dump())                 # {'title': 'Alias Demo', 'content': None}
print("   alias on   ->", w.model_dump(by_alias=True))       # {'post_title': 'Alias Demo', 'content': None}
print("   drop None  ->", w.model_dump(exclude_none=True))   # {'title': 'Alias Demo'}
