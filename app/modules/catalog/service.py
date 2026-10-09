from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.exceptions import NotFoundError, ValidationError
from app.modules.catalog.models import Author, Book, Category
from app.modules.catalog.repository import (
    AuthorRepository,
    BookRepository,
    CategoryRepository,
)
from app.modules.catalog.schemas import (
    AuthorCreate,
    AuthorUpdate,
    BookCreate,
    BookUpdate,
    CategoryCreate,
    CategoryUpdate,
)


class AuthorService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = AuthorRepository(db)

    async def list(self) -> list[Author]:
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


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CategoryRepository(db)

    async def list(self) -> list[Category]:
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


class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repo = BookRepository(db)
        self.author_repo = AuthorRepository(db)
        self.category_repo = CategoryRepository(db)

    async def list(self) -> list[Book]:
        return await self.book_repo.get_all()

    async def get(self, book_id: int) -> Book:
        book = await self.book_repo.get_by_id(book_id)
        if not book:
            raise NotFoundError("Книга не найдена")
        return book

    async def _resolve_categories(self, category_ids: list[int]) -> list[Category]:
        categories = await self.category_repo.get_by_ids(category_ids)
        if len(categories) != len(set(category_ids)):
            raise ValidationError("Некоторые категории не найдены")
        return categories

    async def create(self, data: BookCreate) -> Book:
        if not await self.author_repo.get_by_id(data.author_id):
            raise ValidationError("Автор не найден")

        categories = await self._resolve_categories(data.category_ids)

        payload = data.model_dump(exclude={"category_ids"})
        book = Book(**payload)
        book.categories = categories

        await self.book_repo.add(book)
        await self.db.commit()
        await self.db.refresh(book)

        # Перечитываем с eager-loaded связями
        return await self.get(book.id)

    async def update(self, book_id: int, data: BookUpdate) -> Book:
        book = await self.get(book_id)

        if data.author_id is not None and not await self.author_repo.get_by_id(
            data.author_id
        ):
            raise ValidationError("Автор не найден")

        update_data = data.model_dump(exclude_unset=True, exclude={"category_ids"})
        for key, value in update_data.items():
            setattr(book, key, value)

        if data.category_ids is not None:
            book.categories = await self._resolve_categories(data.category_ids)

        await self.db.commit()
        await self.db.refresh(book)

        return await self.get(book_id)

    async def delete(self, book_id: int) -> None:
        book = await self.get(book_id)
        await self.book_repo.delete(book)
        await self.db.commit()
