from pydantic import BaseModel, ConfigDict, Field


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
