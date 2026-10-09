from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.models import Category


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
