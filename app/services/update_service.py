from aiogram import Bot
from aiogram.types import Update
from pydantic import ValidationError

from app.bot.dispatcher import dispatcher


class TelegramUpdateError(ValueError):
    pass


async def process_webhook_update(bot: Bot, payload: dict[str, object]) -> None:
    try:
        update = Update.model_validate(payload, context={"bot": bot})
    except ValidationError as exc:
        raise TelegramUpdateError("Invalid Telegram update payload.") from exc

    await dispatcher.feed_update(bot, update)
