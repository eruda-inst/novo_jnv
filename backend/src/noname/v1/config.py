from typing import ClassVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    database_url_sync: str = Field(default="...")
    database_url_async: str = Field(default="...")

    timezone: str = Field(default="...")


settings = Settings()
