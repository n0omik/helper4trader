import asyncio
import logging
from aiogram import Bot, Dispatcher
from Config.settings import Config
from aiogram.enums.parse_mode import ParseMode
from Main_bot.handlers.base_handler import router
from Main_bot.commands import set_commands
from aiogram.fsm.storage.redis import RedisStorage



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(Config.TOKEN,parse_mode=ParseMode.HTML)
    await set_commands(bot)
    storage = RedisStorage.from_url(f'redis://localhost:6379/0')
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())




