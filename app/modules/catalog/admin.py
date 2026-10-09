from markupsafe import Markup
from sqladmin import ModelView

from app.modules.catalog.models import Author, Book, Category


class AuthorAdmin(ModelView, model=Author):
    name = "Автор"
    name_plural = "Авторы"
    icon = "fa-solid fa-user-pen"

    column_list = (
        Author.id,
        Author.name,
        Author.description,
        Author.image_url,
    )

    # --- Русские заголовки колонок ---
    column_labels = {
        Author.id: "ID",
        Author.name: "Имя",
        Author.description: "Описание",
        Author.image_url: "Фото (URL)",
        Author.books: "Книги",
    }

    column_searchable_list = (Author.name,)
    column_sortable_list = (Author.id, Author.name)
    column_default_sort = ("id", True)

    column_details_list = (
        Author.id,
        Author.name,
        Author.description,
        Author.image_url,
        Author.books,
    )

    form_columns = (
        Author.name,
        Author.description,
        Author.image_url,
    )

    form_args = {
        "name": {"label": "Имя"},
        "description": {"label": "Описание"},
        "image_url": {"label": "Фото (URL)"},
    }

    can_export = True
    export_types = ["csv"]
    export_max_rows = 1000


class CategoryAdmin(ModelView, model=Category):
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-tags"

    column_list = (
        Category.id,
        Category.name,
        Category.description,
    )

    # --- Русские заголовки колонок ---
    column_labels = {
        Category.id: "ID",
        Category.name: "Название",
        Category.description: "Описание",
        Category.books: "Книги",
    }

    column_searchable_list = (Category.name,)
    column_sortable_list = (Category.id, Category.name)
    column_default_sort = ("id", True)

    column_details_list = (
        Category.id,
        Category.name,
        Category.description,
        Category.books,
    )

    form_columns = (
        Category.name,
        Category.description,
    )

    form_args = {
        "name": {"label": "Название"},
        "description": {"label": "Описание"},
    }

    can_export = True
    export_types = ["csv"]
    export_max_rows = 1000


class BookAdmin(ModelView, model=Book):
    name = "Книга"
    name_plural = "Книги"
    icon = "fa-solid fa-book"

    # --- Список ---
    column_list = (
        Book.id,
        Book.title,
        Book.author,
        Book.categories,
        Book.price,
        Book.discount_percent,
        Book.cover_type,
        Book.release_year,
        Book.pages_count,
    )

    # --- Русские заголовки колонок ---
    column_labels = {
        Book.id: "ID",
        Book.title: "Название",
        Book.author: "Автор",
        Book.categories: "Категории",
        Book.price: "Цена",
        Book.discount_percent: "Скидка",
        Book.cover_type: "Обложка",
        Book.release_year: "Год издания",
        Book.pages_count: "Страниц",
        Book.weight_grams: "Вес (г)",
        Book.dimensions: "Размеры",
        Book.content_summary: "Содержание",
        Book.quotes: "Цитаты",
    }

    column_searchable_list = (Book.title,)
    column_sortable_list = (
        Book.id,
        Book.title,
        Book.price,
        Book.release_year,
    )
    column_default_sort = ("id", True)

    # --- Форматтеры для красивого вывода ---
    column_formatters = {
        Book.author: lambda m, a: m.author.name if m.author else "—",
        Book.categories: lambda m, a: ", ".join(c.name for c in m.categories),
        Book.price: lambda m, a: Markup(f"<b>{m.price} BYN</b>"),
        Book.discount_percent: lambda m, a: (
            f"{m.discount_percent}%" if m.discount_percent else "—"
        ),
        Book.cover_type: lambda m, a: {
            "hard": "Твёрдая",
            "soft": "Мягкая",
            "none": "Нет",
        }.get(
            m.cover_type.value if hasattr(m.cover_type, "value") else m.cover_type,
            "—",
        ),
    }

    # --- Детали ---
    column_details_list = (
        Book.id,
        Book.title,
        Book.author,
        Book.categories,
        Book.price,
        Book.discount_percent,
        Book.cover_type,
        Book.pages_count,
        Book.release_year,
        Book.weight_grams,
        Book.dimensions,
        Book.content_summary,
        Book.quotes,
    )

    # --- Форма ---
    form_columns = (
        Book.title,
        Book.author,
        Book.categories,
        Book.price,
        Book.discount_percent,
        Book.cover_type,
        Book.pages_count,
        Book.release_year,
        Book.weight_grams,
        Book.dimensions,
        Book.content_summary,
        Book.quotes,
    )

    # --- Настройка полей формы ---
    form_args = {
        "title": {
            "label": "Название",
            "description": "Полное название книги",
        },
        "author": {
            "label": "Автор",
        },
        "categories": {
            "label": "Категории",
            "description": "Можно выбрать несколько (Ctrl/Cmd + клик)",
        },
        "price": {
            "label": "Цена (BYN)",
        },
        "discount_percent": {
            "label": "Скидка (%)",
        },
        "cover_type": {
            "label": "Тип обложки",
        },
        "pages_count": {
            "label": "Количество страниц",
        },
        "release_year": {
            "label": "Год издания",
        },
        "weight_grams": {
            "label": "Вес (г)",
        },
        "dimensions": {
            "label": "Размеры",
        },
        "content_summary": {
            "label": "Содержание",
            "description": "Краткое описание содержания книги",
        },
        "quotes": {
            "label": "Цитаты",
            "description": "Избранные цитаты из книги",
        },
    }

    # --- Экспорт ---
    can_export = True
    export_types = ["csv"]
    export_max_rows = 5000
