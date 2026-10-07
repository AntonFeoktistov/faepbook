from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from app.database import engine
from app.modules.users import users_router
from app.modules.users.admin import UserAdmin


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(title="epbook API", lifespan=lifespan)

# Админка
admin = Admin(app, engine)
admin.add_view(UserAdmin)

# Роутеры
app.include_router(users_router)


@app.get("/")
async def root():
    return {"status": "ok", "docs": "/docs", "admin": "/admin"}
