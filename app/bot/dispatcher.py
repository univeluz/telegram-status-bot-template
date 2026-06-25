from aiogram import Dispatcher

from app.bot.handlers import router

dispatcher = Dispatcher()
dispatcher.include_router(router)
