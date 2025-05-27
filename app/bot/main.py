import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from config import bot_settings


bot = Bot(token=bot_settings.token)
dp = Dispatcher()


@dp.message(CommandStart())
async def handle_start(message: types.Message) -> None:
    await message.answer(
        text=f"Привет, {message.from_user.full_name}!\nЭтот бот поможет подобрать тебе самый охуенный тур\nПросто пришли мне город, в который ты хочешь отравиться"
    )


async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
