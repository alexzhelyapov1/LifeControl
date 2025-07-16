# Этап 1: Установка зависимостей в виртуальное окружение
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Этап 2: Финальный образ с приложением
FROM python:3.11-slim

WORKDIR /app

# Создание пользователя без root-прав для безопасности
RUN addgroup --system nonroot && adduser --system --group nonroot

# Копируем "колеса" зависимостей, собранные на предыдущем этапе
COPY --from=builder /wheels /wheels
# Устанавливаем зависимости из "колес"
RUN pip install --no-cache /wheels/*

# Копируем код приложения и конфигурацию Alembic
COPY ./app ./app
COPY ./alembic ./alembic
COPY alembic.ini .

# Меняем владельца всех файлов на пользователя nonroot
RUN chown -R nonroot:nonroot /app

# Переключаемся на пользователя nonroot
USER nonroot

# CMD будет переопределен в docker-compose.yml для гибкости
EXPOSE 8000