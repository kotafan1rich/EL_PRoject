# Используем базовый образ Python
FROM python:3.9-slim

RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt install tzdata
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

RUN chmod a+x docker/*.sh
