from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models import Author


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
