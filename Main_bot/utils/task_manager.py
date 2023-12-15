from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.redis import RedisJobStore


storage = {
    'default':RedisJobStore(
        jobs_key="tasks",
        run_times_key='tasks_running',
        host = "localhost",
        port = 6379,
        db=2
    )
}

schedueler = AsyncIOScheduler(timezone= 'Europe/Berlin', jobstores = storage)


