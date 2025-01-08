#!/bin/bash

# Параметры
CONTAINER_NAME="postgres"          # Название контейнера из docker-compose.yml
BACKUP_DIR="./postgres/backups"             # Папка с бэкапами
POSTGRES_USER="postgres"           # Имя пользователя PostgreSQL
POSTGRES_DB="min_db"               # Имя базы данных
POSTGRES_PASSWORD="2007Fj2007"     # Пароль пользователя

# Проверяем наличие папки с бэкапами
if [ ! -d "$BACKUP_DIR" ]; then
  echo "Папка с бэкапами не найдена: $BACKUP_DIR"
  exit 1
fi

# Вывод списка доступных бэкапов
echo "Доступные бэкапы:"
ls -1 $BACKUP_DIR/*.sql || { echo "Нет бэкапов в папке $BACKUP_DIR"; exit 1; }

# Просим пользователя выбрать файл
echo -n "Введите имя файла для восстановления (с расширением .sql): "
read BACKUP_FILE

# Проверяем, существует ли указанный файл
if [ ! -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
  echo "Файл не найден: $BACKUP_DIR/$BACKUP_FILE"
  exit 1
fi

# Выполняем восстановление базы данных
echo "Начинаем восстановление базы данных из файла $BACKUP_DIR/$BACKUP_FILE..."


# Сброс всех таблиц
echo "Удаляем существующие таблицы..."
docker exec -e PGPASSWORD=$POSTGRES_PASSWORD -i $CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

if [ $? -eq 0 ]; then
    echo "Все таблицы успешно удалены."
else
    echo "Ошибка при удалении таблиц. Проверьте соединение или права доступа."
    exit 1
fi

docker exec -e PGPASSWORD=$POSTGRES_PASSWORD -i $CONTAINER_NAME psql -U $POSTGRES_USER -d $POSTGRES_DB < "$BACKUP_DIR/$BACKUP_FILE"

# Проверяем успешность выполнения
if [ $? -eq 0 ]; then
  echo "Восстановление успешно завершено."
else
  echo "Ошибка восстановления базы данных."
fi
