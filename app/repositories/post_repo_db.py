from typing import List, Optional
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.post import Post
from app.schemas.post import PostCreate, PostOut,PostUpdate


class PostDBRepo:
    def __init__(self,session: AsyncSession) -> None:
        self.session = session

    async def list(self) -> List[PostOut]:
        stmt = select(Post).order_by(Post.id)
        res = await self.session.execute(stmt)
        rows = res.scalars().all()
        result = []
        for r in rows:
            result.append(PostOut(id=r.id,content=r.content,title=r.title))
        return result

    async def get(self,post_id) -> Optional[PostOut]:
        row = await self.session.get(Post,post_id)
        if not row:
            return None
        return PostOut(id=row.id,content=row.content,title=row.title)
    
    async def create(self,payload: PostCreate) -> PostOut:
        row = Post(**payload.model_dump())
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return PostOut(id=row.id,title=row.title,content=row.content)

    async def update(self, post_id: int,payload: PostUpdate) -> PostOut:
        patch = payload.model_dump(exclude_unset=True)
        if not patch:
            current = await self.session.get(Post,post_id)
            if not current:
                return None
            return PostOut(id=current.id, title=current.title, content=current.content)
        stmt = (
            update(Post)
            .where(Post.id == post_id)
            .values(**patch)
            .returning(Post.id, Post.title, Post.content)
        )
        res = await self.session.execute(stmt)
        row = res.first()
        if not row:
            await self.session.rollback()
            return None
        await self.session.commit()
        rid, title, content = row
        return PostOut(id=rid, title=title, content=content)

    async def delete(self, post_id: int) -> bool:
        stmt = delete(Post).where(Post.id == post_id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return res.rowcount > 0