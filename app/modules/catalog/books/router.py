from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.catalog.books.schemas import (
    BookCreate,
    BookResponse,
    BookUpdate,
)
from app.modules.catalog.books.service import BookService
from app.modules.users.auth import get_current_admin
from app.modules.users.models import User

router = APIRouter(prefix="/api/v1/books", tags=["books"])


@router.get("/", response_model=list[BookResponse])
async def get_all_books(db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.get_all()


@router.get("/{book_id}/", response_model=BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    service = BookService(db)
    return await service.get(book_id)


@router.post("/", response_model=BookResponse, status_code=201)
async def create_book(
    data: BookCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = BookService(db)
    return await service.create(data)


@router.patch("/{book_id}/", response_model=BookResponse)
async def update_book(
    book_id: int,
    data: BookUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = BookService(db)
    return await service.update(book_id, data)


@router.delete("/{book_id}/", status_code=204)
async def delete_book(
    book_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = BookService(db)
    await service.delete(book_id)
