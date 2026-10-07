from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    password2: str = Field(min_length=8, max_length=128)

    @field_validator("password2")
    @classmethod
    def passwords_match(cls, v, info):
        if info.data.get("password") != v:
            raise ValueError("Пароли не совпадают")
        return v


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access: str
    refresh: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    first_name: str
    last_name: str
    is_active: bool
    is_admin: bool
    created_at: datetime

    model_config = {"from_attributes": True}
