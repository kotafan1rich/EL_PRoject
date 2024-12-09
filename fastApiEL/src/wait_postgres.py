import asyncio
import asyncpg
import sys

from config import (
	POSTGRES_PASSWORD,
	POSTGRES_NAME,
	POSTGRES_USER,
	POSTGRES_HOST,
	POSTGRES_PORT,
)


async def check_postgres():
	try:
		conn = await asyncpg.connect(
			user=POSTGRES_USER,
			password=POSTGRES_PASSWORD,
			database=POSTGRES_NAME,
			host=POSTGRES_HOST,
			port=POSTGRES_PORT,
		)
		await conn.close()
		print("PostgreSQL is ready!")
		return True
	except Exception as e:
		print(f"Waiting for PostgreSQL: {e}")
		return False


async def main():
	for _ in range(30):  # Попытаться подключиться 30 раз
		if await check_postgres():
			sys.exit(0)
		await asyncio.sleep(1)
	sys.exit(1)  # Если за 30 попыток база не стала доступна


if __name__ == "__main__":
	asyncio.run(main())
