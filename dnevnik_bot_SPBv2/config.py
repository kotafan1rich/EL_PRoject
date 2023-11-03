import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
