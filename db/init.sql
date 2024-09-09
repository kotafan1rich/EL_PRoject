-- Создаем пользователя для миграций
-- CREATE USER maigrator WITH PASSWORD 'postgres';

-- Назначаем права для подключения к базе данных
GRANT pg_execute_server_program TO postgres;
