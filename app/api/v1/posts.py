

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.post_repo_db import PostDBRepo
from app.repositories.post_repo import PostRepo
from app.repositories.post_repo import repo, PostRepo
from app.schemas.post import PostOut,PostCreate, PostUpdate


router = APIRouter()

# def get_repo() -> PostRepo:
#     return repo


def get_repo(session: AsyncSession = Depends(get_session)) -> PostDBRepo:
    return PostDBRepo(session)


@router.get('/',response_model=List[PostOut])
async def list_posts(r: PostDBRepo = Depends(get_repo)):
    return await r.list()

@router.get('/{post_id}',response_model=PostOut)
async def get_post(post_id:int, r:PostRepo = Depends(get_repo)):
    post = await r.get(post_id)
    if not post:
        raise HTTPException(status_code=404,detail="Post not found")
    return post

@router.post('/',response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def craete_post(payload: PostCreate,r:PostDBRepo = Depends(get_repo)):
    return await r.create(payload)

@router.put("/{post_id}",response_model=PostOut)
async def update_post(post_id: int, payload: PostUpdate,r:PostDBRepo = Depends(get_repo)):
    updated = await r.update(post_id,payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated

@router.delete("/{post_id}", status_code= status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, r: PostDBRepo = Depends(get_repo)):
    ok = await r.delete(post_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Post not found")
    return None