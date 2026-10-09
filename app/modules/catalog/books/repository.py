from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.catalog.models import Book


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _base_query(self):
        return select(Book).options(
            selectinload(Book.author),
            selectinload(Book.categories),
        )

    async def get_all(self) -> list[Book]:
        result = await self.db.execute(self._base_query().order_by(Book.id))
        return list(result.scalars().all())

    async def get_by_id(self, book_id: int) -> Book | None:
        result = await self.db.execute(self._base_query().where(Book.id == book_id))
        return result.scalar_one_or_none()

    async def add(self, book: Book) -> Book:
        self.db.add(book)
        return book

    async def delete(self, book: Book) -> None:
        await self.db.delete(book)
