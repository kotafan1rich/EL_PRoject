#!/bin/bash

# Параметры
CONTAINER_NAME="postgres"          # Название контейнера из docker-compose.yml
BACKUP_DIR="./postgres/backups"             # Папка для хранения бэкапов
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S") # Метка времени
BACKUP_FILE="$BACKUP_DIR/db_backup_$TIMESTAMP.sql"

# Данные для подключения
POSTGRES_USER="postgres"           # Имя пользователя PostgreSQL
POSTGRES_DB="min_db"               # Имя базы данных
POSTGRES_PASSWORD="2007Fj2007"     # Пароль пользователя

# Проверяем, существует ли папка для бэкапов, если нет — создаем
if [ ! -d "$BACKUP_DIR" ]; then
  mkdir -p "$BACKUP_DIR"
fi

# Выполняем команду создания бэкапа с использованием пароля
docker exec -e PGPASSWORD=$POSTGRES_PASSWORD -t $CONTAINER_NAME pg_dump -U $POSTGRES_USER -d $POSTGRES_DB > $BACKUP_FILE

# Проверяем успешность создания бэкапа
if [ $? -eq 0 ]; then
  echo "Бэкап успешно сохранен: $BACKUP_FILE"
else
  echo "Ошибка создания бэкапа"
  # Удаляем файл, если он пустой
  [ -e "$BACKUP_FILE" ] && rm "$BACKUP_FILE"
fi
