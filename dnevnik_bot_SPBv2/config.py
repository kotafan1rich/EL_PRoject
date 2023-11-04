import os

from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv('DEBUG')

TOKEN = os.getenv('TEST_TOKEN') if DEBUG == 'True' else os.getenv('TOKEN')
API_HOST = os.getenv('API_HOST')
API_PORT = os.getenv('API_PORT')
