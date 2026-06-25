import os

import pytest

from app.config.settings import get_settings


@pytest.fixture(autouse=True)
def configure_test_environment() -> None:
    os.environ["BOT_TOKEN"] = "123456:TEST_TOKEN"
    os.environ["APP_URL"] = "https://example.com"
    os.environ["WEBHOOK_SECRET_TOKEN"] = "test-secret-token"
    os.environ["START_MESSAGE"] = "Bot is ready."
    os.environ["SYNC_WEBHOOK_ON_STARTUP"] = "false"
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
