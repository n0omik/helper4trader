import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from Config.settings import Config
from aiogram.enums.parse_mode import ParseMode
from Main_bot.handlers.base_handler import router
from Main_bot.commands import set_commands
from aiogram.fsm.storage.redis import RedisStorage
from Main_bot.utils.task_manager import schedueler

task_router = Router()

@task_router.message(Command('start_schadueler'))
async def run_taskmanager(message:Message):
    schedueler.start()

@task_router.message(Command('shutdown'))
async def stop_taskmanager(message:Message):
    schedueler.shutdown(wait=True)
    schedueler.remove_all_jobs()

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(Config.TOKEN,parse_mode=ParseMode.HTML)
    await set_commands(bot)
    storage = RedisStorage.from_url(f'redis://localhost:6379/0')
    dp = Dispatcher(storage=storage)
    schedueler.ctx.add_instance(bot,declared_class=Bot)
    dp.include_routers(router,task_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())




