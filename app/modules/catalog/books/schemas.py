from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field

from app.modules.catalog.authors.schemas import AuthorResponse
from app.modules.catalog.categories.schemas import CategoryResponse


class CoverType(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    NONE = "none"


class BookBase(BaseModel):
    title: str = Field(max_length=256)
    author_id: int
    price: Decimal = Field(ge=0)
    discount_percent: Decimal | None = Field(default=None, ge=0, le=100)
    cover_type: CoverType = CoverType.SOFT
    pages_count: int | None = None
    release_year: int | None = None
    weight_grams: int | None = None
    dimensions: str | None = None
    content_summary: str | None = None
    quotes: str | None = None


class BookCreate(BookBase):
    category_ids: list[int] = []


class BookUpdate(BaseModel):
    title: str | None = None
    author_id: int | None = None
    price: Decimal | None = None
    discount_percent: Decimal | None = None
    cover_type: CoverType | None = None
    pages_count: int | None = None
    release_year: int | None = None
    weight_grams: int | None = None
    dimensions: str | None = None
    content_summary: str | None = None
    quotes: str | None = None
    category_ids: list[int] | None = None


class BookResponse(BookBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author: AuthorResponse
    categories: list[CategoryResponse] = []
