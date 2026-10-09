from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.categories.repository import CategoryRepository
from app.modules.catalog.categories.schemas import CategoryCreate, CategoryUpdate
from app.modules.catalog.exceptions import NotFoundError
from app.modules.catalog.models import Category


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CategoryRepository(db)

    async def get_all(self) -> list[Category]:
        return await self.repo.get_all()

    async def get(self, category_id: int) -> Category:
        category = await self.repo.get_by_id(category_id)
        if not category:
            raise NotFoundError("Категория не найдена")
        return category

    async def create(self, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())
        await self.repo.add(category)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def update(self, category_id: int, data: CategoryUpdate) -> Category:
        category = await self.get(category_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)
        await self.db.commit()
        await self.db.refresh(category)
        return category

    async def delete(self, category_id: int) -> None:
        category = await self.get(category_id)
        await self.repo.delete(category)
        await self.db.commit()
