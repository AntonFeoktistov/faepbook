from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.catalog.models import Author, Book, Category


class AuthorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Author]:
        result = await self.db.execute(select(Author).order_by(Author.id))
        return list(result.scalars().all())

    async def get_by_id(self, author_id: int) -> Author | None:
        return await self.db.get(Author, author_id)

    async def add(self, author: Author) -> Author:
        self.db.add(author)
        return author

    async def delete(self, author: Author) -> None:
        await self.db.delete(author)


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Category]:
        result = await self.db.execute(select(Category).order_by(Category.id))
        return list(result.scalars().all())

    async def get_by_id(self, category_id: int) -> Category | None:
        return await self.db.get(Category, category_id)

    async def get_by_ids(self, ids: list[int]) -> list[Category]:
        if not ids:
            return []
        result = await self.db.execute(select(Category).where(Category.id.in_(ids)))
        return list(result.scalars().all())

    async def add(self, category: Category) -> Category:
        self.db.add(category)
        return category

    async def delete(self, category: Category) -> None:
        await self.db.delete(category)


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Book]:
        result = await self.db.execute(
            select(Book)
            .options(selectinload(Book.author), selectinload(Book.categories))
            .order_by(Book.id)
        )
        return list(result.scalars().all())

    async def get_by_id(self, book_id: int) -> Book | None:
        result = await self.db.execute(
            select(Book)
            .options(selectinload(Book.author), selectinload(Book.categories))
            .where(Book.id == book_id)
        )
        return result.scalar_one_or_none()

    async def add(self, book: Book) -> Book:
        self.db.add(book)
        return book

    async def delete(self, book: Book) -> None:
        await self.db.delete(book)
