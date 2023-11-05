# Используем базовый образ Python
FROM python:3.9
RUN mkdir /fastapi_app

WORKDIR /fastapi_app

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install -r requirements.txt


# Копируем исходный код бота в контейнер
COPY . .


# Команда для запуска бота
CMD ["python", "main.py"]
