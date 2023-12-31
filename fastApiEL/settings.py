from envparse import Env
from config import POSTGRES_HOST, POSTGRES_NAME, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER

env = Env()

REAL_DATABASE_URL = env.str(
    "REAL_DATABASE_URL",
    default=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_NAME}"
)  # connect string for the database
