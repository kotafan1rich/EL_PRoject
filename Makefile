API_IMAGE_NAME = my_api

API_PORT = 8000
POSTGRES_PORT = 5432

API_DIR = ./fastApiEL
DOCKER_COMPOSE_FILE = ./docker-compose.yaml

build:
	docker-compose -f $(DOCKER_COMPOSE_FILE) build

up:
	docker-compose -f $(DOCKER_COMPOSE_FILE) up -d

down:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down

logs:
	docker-compose -f $(DOCKER_COMPOSE_FILE) logs -f

clean:
	docker-compose -f $(DOCKER_COMPOSE_FILE) down --volumes --rmi all

migrate:
	docker exec -it api alembic upgrade head

makemigrations:
	docker exec -it api alembic revision --autogenerate -m "chande auto"


rebuild: down build up

help:
	@echo "Доступные цели:"
	@echo "  build       - Собрать Docker контейнеры"
	@echo "  up          - Запустить Docker контейнеры в фоновом режиме"
	@echo "  down        - Остановить и удалить Docker контейнеры"
	@echo "  logs        - Просмотреть логи Docker контейнеров"
	@echo "  clean       - Удалить все контейнеры, образы и тома (осторожно!)"
	@echo "  rebuild     - Пересобрать и перезапустить Docker контейнеры"
