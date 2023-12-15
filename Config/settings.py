import os
from dotenv import load_dotenv, find_dotenv
from dataclasses import dataclass
load_dotenv(find_dotenv())

@dataclass
class RedisConfig:
    HOST = "localhost"
    PORT = 6379
    DB = 0

    def get_url(self):
        return f"redis://{self.HOST}:{self.PORT}/{self.DB}"
@dataclass
class Config:
    TOKEN = os.getenv("TOKEN")
    BINANCE_KEY = os.getenv("BINANCE_KEY")
    BINANCE_SECRET = os.getenv("BINANCE_SECRET")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    DATABASE_URL = ""


