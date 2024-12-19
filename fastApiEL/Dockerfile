# Используем базовый образ Python
FROM python:3.9

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
