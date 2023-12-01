import asyncio
import logging
from aiogram import Bot, Dispatcher
from Config.settings import TOKEN
from aiogram.enums.parse_mode import ParseMode
from Main_bot.handlers.base_handler import router
from Main_bot.commands import set_commands


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(TOKEN,parse_mode=ParseMode.HTML)
    await set_commands(bot)
    dp = Dispatcher()
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())




