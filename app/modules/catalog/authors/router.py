from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.catalog.authors.schemas import (
    AuthorCreate,
    AuthorResponse,
    AuthorUpdate,
)
from app.modules.catalog.authors.service import AuthorService
from app.modules.users.auth import get_current_admin
from app.modules.users.models import User

router = APIRouter(prefix="/api/v1/authors", tags=["authors"])


@router.get("/", response_model=list[AuthorResponse])
async def get_all_authors(db: AsyncSession = Depends(get_db)):
    service = AuthorService(db)
    return await service.get_all()


@router.get("/{author_id}/", response_model=AuthorResponse)
async def get_author(author_id: int, db: AsyncSession = Depends(get_db)):
    service = AuthorService(db)
    return await service.get(author_id)


@router.post("/", response_model=AuthorResponse, status_code=201)
async def create_author(
    data: AuthorCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = AuthorService(db)
    return await service.create(data)


@router.patch("/{author_id}/", response_model=AuthorResponse)
async def update_author(
    author_id: int,
    data: AuthorUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = AuthorService(db)
    return await service.update(author_id, data)


@router.delete("/{author_id}/", status_code=204)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = AuthorService(db)
    await service.delete(author_id)
