-- Создаем пользователя для миграций
-- CREATE USER maigrator WITH PASSWORD 'postgres';

-- Назначаем права для подключения к базе данных
GRANT CONNECT ON DATABASE postgres TO postgres;

-- Назначаем права на работу с таблицами и последовательностями в схеме public
GRANT USAGE ON SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO postgres;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO postgres;

-- Разрешаем пользователю создавать объекты в схеме public
GRANT CREATE ON SCHEMA public TO postgres;
