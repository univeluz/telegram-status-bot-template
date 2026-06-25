from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from app.services.message_service import get_start_message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(get_start_message())
