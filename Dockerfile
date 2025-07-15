# Этап 1: Установка зависимостей
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# Этап 2: Финальный образ
FROM python:3.11-slim as final

WORKDIR /app

# Создание пользователя без root-прав
RUN addgroup --system nonroot && adduser --system --group nonroot

# Копируем зависимости из builder'а
COPY --from=builder /wheels /wheels
RUN pip install --no-cache /wheels/*

# Копируем код приложения
COPY ./app /app/app
COPY ./alembic /app/alembic
COPY alembic.ini /app/

# Меняем владельца файлов на nonroot
RUN chown -R nonroot:nonroot /app

# Переключаемся на пользователя nonroot
USER nonroot

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]