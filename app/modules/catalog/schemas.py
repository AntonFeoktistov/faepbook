from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class CoverType(str, Enum):
    HARD = "hard"
    SOFT = "soft"
    NONE = "none"


# ---------- Author ----------


class AuthorBase(BaseModel):
    name: str = Field(max_length=128)
    description: str | None = None
    image_url: str | None = None


class AuthorCreate(AuthorBase):
    pass


class AuthorUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    image_url: str | None = None


class AuthorResponse(AuthorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# ---------- Category ----------


class CategoryBase(BaseModel):
    name: str = Field(max_length=64)
    description: str | None = None


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# ---------- Book ----------


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
    category_ids: list[int] = []


class BookCreate(BookBase):
    pass


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
