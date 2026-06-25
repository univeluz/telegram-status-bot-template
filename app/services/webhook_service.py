import logging

from aiogram import Bot

from app.config.settings import Settings

logger = logging.getLogger(__name__)


async def sync_webhook_on_startup(bot: Bot, settings: Settings) -> None:
    if not settings.sync_webhook_on_startup:
        logger.warning("Webhook synchronization on startup is disabled")
        return

    if settings.delete_webhook_before_set:
        await bot.delete_webhook(
            drop_pending_updates=settings.drop_pending_updates_on_startup,
        )
        logger.info("Existing Telegram webhook deleted before synchronization")

    await bot.set_webhook(
        url=settings.webhook_url,
        secret_token=settings.webhook_secret_token,
        drop_pending_updates=settings.drop_pending_updates_on_startup,
    )
    logger.info("Telegram webhook synchronized")


async def sync_webhook_on_shutdown(bot: Bot, settings: Settings) -> None:
    if not settings.delete_webhook_on_shutdown:
        return

    await bot.delete_webhook(drop_pending_updates=False)
    logger.info("Telegram webhook deleted on shutdown")


async def close_bot_session(bot: Bot) -> None:
    await bot.session.close()
