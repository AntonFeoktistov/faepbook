from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- FastAPI ---
    debug: bool = Field(default=False, description="Режим отладки")
    secret_key: str = Field(default="unsafe", description="Секрет приложения")

    # --- PostgreSQL ---
    postgres_db: str = Field(default="epbook")
    postgres_user: str = Field(default="epbook")
    postgres_password: str = Field(default="epbook")
    postgres_host: str = Field(default="db")
    postgres_port: int = Field(default=5432)

    # --- JWT ---
    jwt_secret: str = Field(
        default="unsafe-jwt", description="Секрет для подписи токенов"
    )
    jwt_algorithm: str = Field(default="HS256")
    jwt_access_expire_minutes: int = Field(default=60)
    jwt_refresh_expire_days: int = Field(default=7)

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:"
            f"{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
