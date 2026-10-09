from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqladmin import Admin

from app.database import engine
from app.modules.catalog.authors.router import router as authors_router
from app.modules.catalog.books.router import router as books_router
from app.modules.catalog.categories.router import router as categories_router
from app.modules.catalog.exceptions import NotFoundError, ValidationError
from app.modules.users import users_router
from app.modules.users.admin import UserAdmin


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="epbook API", lifespan=lifespan)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


# Админка
admin = Admin(app, engine)
admin.add_view(UserAdmin)

# Роутеры
app.include_router(users_router)
app.include_router(authors_router)
app.include_router(categories_router)
app.include_router(books_router)


@app.get("/")
async def root():
    return {"status": "ok", "docs": "/docs", "admin": "/admin"}
