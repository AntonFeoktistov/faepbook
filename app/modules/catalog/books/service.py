from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.catalog.authors.repository import AuthorRepository
from app.modules.catalog.books.repository import BookRepository
from app.modules.catalog.books.schemas import BookCreate, BookUpdate
from app.modules.catalog.categories.repository import CategoryRepository
from app.modules.catalog.exceptions import NotFoundError, ValidationError
from app.modules.catalog.models import Book, Category


class BookService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.book_repo = BookRepository(db)
        self.author_repo = AuthorRepository(db)
        self.category_repo = CategoryRepository(db)

    async def get_all(self) -> list[Book]:
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

    async def _validate_author(self, author_id: int) -> None:
        if not await self.author_repo.get_by_id(author_id):
            raise ValidationError("Автор не найден")

    async def create(self, data: BookCreate) -> Book:
        await self._validate_author(data.author_id)
        categories = await self._resolve_categories(data.category_ids)

        payload = data.model_dump(exclude={"category_ids"})
        book = Book(**payload)
        book.categories = categories

        await self.book_repo.add(book)
        await self.db.commit()

        return await self.get(book.id)

    async def update(self, book_id: int, data: BookUpdate) -> Book:
        book = await self.get(book_id)

        if data.author_id is not None:
            await self._validate_author(data.author_id)

        update_data = data.model_dump(exclude_unset=True, exclude={"category_ids"})
        for key, value in update_data.items():
            setattr(book, key, value)

        if data.category_ids is not None:
            book.categories = await self._resolve_categories(data.category_ids)

        await self.db.commit()
        return await self.get(book_id)

    async def delete(self, book_id: int) -> None:
        book = await self.get(book_id)
        await self.book_repo.delete(book)
        await self.db.commit()
