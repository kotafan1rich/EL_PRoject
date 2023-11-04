import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from dotenv import load_dotenv

from config import TOKEN

load_dotenv()


storage = MemoryStorage()

bot = Bot(token=TOKEN, parse_mode='HTML')
dp = Dispatcher(storage=storage)
