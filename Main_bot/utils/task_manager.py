from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore
from Main_bot.utils.pars_news import pars_news
import random
from apscheduler_di import ContextSchedulerDecorator

storage = {
    'default':RedisJobStore(
        jobs_key="tasks",
        run_times_key='tasks_running',
        host = "localhost",
        port = 6379,
        db=2
    )
}

schedueler = ContextSchedulerDecorator(AsyncIOScheduler(timezone= 'Europe/Berlin', jobstores = storage))
schedueler.add_job(pars_news,'interval',seconds=60,name='pars_news')

def random_price():
    price = random.randint(1,5)
    print(price)
    return price

async def send_notification(bot:Bot, price:float, chat_id):
    if random_price() == price:
        await bot.send_message(chat_id, text="i'm working")

def set_alert_job(price, chat_id):
    schedueler.add_job(send_notification, 'interval', seconds = 1, kwargs={'price':price, 'chat_id':chat_id})
