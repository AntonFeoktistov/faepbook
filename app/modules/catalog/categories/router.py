from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.modules.catalog.categories.schemas import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.modules.catalog.categories.service import CategoryService
from app.modules.users.auth import get_current_admin
from app.modules.users.models import User

router = APIRouter(prefix="/api/v1/categories", tags=["categories"])


@router.get("/", response_model=list[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get_all()


@router.get("/{category_id}/", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    service = CategoryService(db)
    return await service.get(category_id)


@router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = CategoryService(db)
    return await service.create(data)


@router.patch("/{category_id}/", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = CategoryService(db)
    return await service.update(category_id, data)


@router.delete("/{category_id}/", status_code=204)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    _: User = Depends(get_current_admin),
):
    service = CategoryService(db)
    await service.delete(category_id)
