"""
Единственная цель этого файла — импортировать все модели,
чтобы Alembic видел их в Base.metadata.
При добавлении нового модуля — добавляйте импорт сюда.
"""

from app.modules.catalog.models import Author, Book, Category
from app.modules.users.models import User

__all__ = ("Author", "Book", "Category", "User")
