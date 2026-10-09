from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.authors.repository import AuthorRepository
from app.modules.catalog.authors.schemas import AuthorCreate, AuthorUpdate
from app.modules.catalog.exceptions import NotFoundError
from app.modules.catalog.models import Author


class AuthorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthorRepository(db)

    async def get_all(self) -> list[Author]:
        return await self.repo.get_all()

    async def get(self, author_id: int) -> Author:
        author = await self.repo.get_by_id(author_id)
        if not author:
            raise NotFoundError("Автор не найден")
        return author

    async def create(self, data: AuthorCreate) -> Author:
        author = Author(**data.model_dump())
        await self.repo.add(author)
        await self.db.commit()
        await self.db.refresh(author)
        return author

    async def update(self, author_id: int, data: AuthorUpdate) -> Author:
        author = await self.get(author_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(author, key, value)
        await self.db.commit()
        await self.db.refresh(author)
        return author

    async def delete(self, author_id: int) -> None:
        author = await self.get(author_id)
        await self.repo.delete(author)
        await self.db.commit()
