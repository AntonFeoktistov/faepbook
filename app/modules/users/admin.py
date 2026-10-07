from sqladmin import ModelView

from app.modules.users.models import User


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = (
        User.id,
        User.username,
        User.email,
        User.is_active,
        User.is_admin,
        User.is_superuser,
    )
    column_searchable_list = (User.username, User.email)
    column_default_sort = ("id", True)
    form_columns = (
        User.username,
        User.email,
        User.hashed_password,
        User.first_name,
        User.last_name,
        User.is_active,
        User.is_admin,
        User.is_superuser,
    )
