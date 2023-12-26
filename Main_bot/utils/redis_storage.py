from redis import  Redis
from Config.settings import RedisConfig

storage = Redis(
    host=RedisConfig.HOST,
    port=RedisConfig.PORT,
    db=3,
    decode_responses=True,
)

