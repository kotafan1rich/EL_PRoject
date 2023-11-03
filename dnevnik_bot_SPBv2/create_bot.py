import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

load_dotenv()


TOKEN = os.getenv('TOKEN')
storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)
