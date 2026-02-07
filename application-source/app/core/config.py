"""Application configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Environment-driven application settings."""

    PROJECT_NAME: str = "Dairy Hub API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "User#2025"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "dairy_hub"

    # SQLAlchemy database URL
    # Default to a local SQLite file. You can override by setting the DATABASE_URL
    # environment variable (for example: postgresql://...)
    DATABASE_URL: str = "sqlite:///./app/database/dairy_hub.db"

    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
