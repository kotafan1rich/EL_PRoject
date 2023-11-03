# Используем базовый образ Python
FROM python:3.9

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt
# aiofiles==23.1.0 aiohttp==3.8.6 aiosignal==1.3.1 alembic==1.9.0 annotated-types==0.6.0 anyio==3.7.1 async-timeout==4.0.3 asyncpg==0.27.0 attrs==23.1.0 bcrypt==4.0.1 certifi==2023.7.22 cfgv==3.4.0 charset-normalizer==3.3.2 click==8.1.7 colorama==0.4.6 distlib==0.3.7 ecdsa==0.18.0 envparse==0.2.0 exceptiongroup==1.1.3 fastapi==0.88.0 filelock==3.13.1 frozenlist==1.4.0 greenlet==2.0.2 h11==0.14.0 httpcore==0.16.3 httpx==0.23.3 identify==2.5.31 idna==3.4 magic-filter==1.0.12 Mako==1.2.4 MarkupSafe==2.1.3 multidict==6.0.4 nodeenv==1.8.0 passlib==1.7.4 platformdirs==3.11.0 pre-commit==2.21.0 prometheus-client==0.18.0 psycopg2-binary==2.9.5 pyasn1==0.5.0 pydantic pydantic_core==2.6.3 python-dotenv==1.0.0 python-jose==3.3.0 python-multipart==0.0.5 PyYAML==6.0.1 requests==2.31.0 rfc3986==1.5.0 rsa==4.9 sentry-sdk==1.33.1 six==1.16.0 sniffio==1.3.0 SQLAlchemy==1.4.45 starlette==0.22.0 starlette-exporter==0.15.1  typing_extensions==4.7.1 urllib3==2.0.7 uvicorn==0.20.0 virtualenv==20.24.6 yarl==1.9.2


# Копируем исходный код API в контейнер
COPY . .

# Указываем рабочую директорию
RUN chmod a+x docker/*.sh

# Команда для запуска API с помощью Uvicorn
