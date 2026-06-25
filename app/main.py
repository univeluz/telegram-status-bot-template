import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from aiogram import Bot
from fastapi import FastAPI

from app.api.routes import router
from app.config.logging import configure_logging
from app.config.settings import get_settings
from app.services.webhook_service import (
    close_bot_session,
    sync_webhook_on_shutdown,
    sync_webhook_on_startup,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level)
    bot = Bot(token=settings.bot_token)
    application.state.settings = settings
    application.state.bot = bot

    try:
        await sync_webhook_on_startup(bot, settings)
        logger.info("Application startup completed")
        yield
    finally:
        await sync_webhook_on_shutdown(bot, settings)
        await close_bot_session(bot)
        logger.info("Application shutdown completed")


app = FastAPI(title="Telegram Status Bot Template", lifespan=lifespan)
app.include_router(router)
