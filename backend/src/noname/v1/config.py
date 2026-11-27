from typing import ClassVar

from pydantic import Field, PositiveInt, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    database_url_sync: str = Field(default="...")
    database_url_async: str = Field(default="...")

    jwt_access_token_expire_minutes: PositiveInt = Field(default=1)
    jwt_algorithm: str = Field(default="...")
    jwt_refresh_token_expire_days: PositiveInt = Field(default=1)
    jwt_secret_key: SecretStr = Field(default=SecretStr("..."))

    timezone: str = Field(default="...")

    @computed_field()
    @property
    def jwt_token_expire_seconds(self) -> PositiveInt:
        return self.jwt_access_token_expire_minutes * 60


settings = Settings()
