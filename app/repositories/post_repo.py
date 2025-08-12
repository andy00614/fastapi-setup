from typing import Dict, List, Optional

from app.schemas.post import PostCreate, PostOut, PostUpdate

class PostRepo:
    def __init__(self) -> None:
        self._data: Dict[int, PostOut] = {}
        self._next_id = 1

    def list(self) -> List[PostOut]:
        return list(self._data.values())

    # TODO:这里一会看一下post_id是怎么传递进来的
    def get(self,post_id: int) -> Optional[PostOut]:
        return self._data.get(post_id)

    def create(self,payload: PostCreate) -> PostOut:
        post = PostOut(id=self._next_id, **payload.model_dump())
        self._data[self._next_id] = post
        self._next_id += 1
        return post

    def update(self, post_id: int, payload: PostUpdate) -> Optional[PostOut]:
        old = self._data.get(post_id)
        if not old:
            return None
        data = old.model_dump()
        patch = payload.model_dump(exclude_unset=True)
        data.update(patch)
        newData = PostOut(**data)
        self._data[post_id] = newData
        return newData
    
    def delete(self,post_id) -> Optional[PostOut]:
        return self._data.pop(post_id,None) is not None

repo = PostRepo()