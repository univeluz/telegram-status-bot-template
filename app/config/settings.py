from functools import lru_cache

from pydantic import AnyHttpUrl, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    service_name: str = Field(default="telegram-status-bot")
    environment: str = Field(default="production")
    bot_token: str
    app_url: AnyHttpUrl
    webhook_secret_token: str
    start_message: str
    webhook_path: str = Field(default="/webhook")
    drop_pending_updates_on_startup: bool = Field(default=False)
    delete_webhook_before_set: bool = Field(default=True)
    delete_webhook_on_shutdown: bool = Field(default=False)
    sync_webhook_on_startup: bool = Field(default=True)
    log_level: str = Field(default="INFO")

    @field_validator("webhook_path")
    @classmethod
    def validate_webhook_path(cls, value: str) -> str:
        if not value.startswith("/"):
            raise ValueError("WEBHOOK_PATH must start with '/'.")
        if value != "/webhook":
            raise ValueError("Only /webhook is allowed by this template.")
        return value

    @field_validator("webhook_secret_token", "start_message")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Value must not be empty.")
        return value

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        normalized = value.upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if normalized not in allowed:
            raise ValueError("LOG_LEVEL must be a valid Python logging level.")
        return normalized

    @property
    def webhook_url(self) -> str:
        return f"{str(self.app_url).rstrip('/')}{self.webhook_path}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
