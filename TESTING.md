# Тестирование LifeControl

## Быстрое тестирование

После запуска приложения вы можете протестировать его функциональность:

### 1. Проверка доступности сервисов

```bash
# Проверка API
curl http://localhost:8000/docs

# Проверка Frontend
curl http://localhost:3000

# Проверка базы данных
sudo docker compose exec db psql -U financier -d financier -c "SELECT version();"
```

### 2. Тестирование API через Swagger UI

1. Откройте http://localhost:8000/docs в браузере
2. Найдите эндпоинт `POST /api/v1/auth/token`
3. Нажмите "Try it out"
4. Введите данные для входа:
   - **username**: admin
   - **password**: admin123
5. Нажмите "Execute"
6. Скопируйте полученный токен

### 3. Тестирование защищенных эндпоинтов

1. В Swagger UI нажмите кнопку "Authorize"
2. Введите токен в формате: `Bearer <your_token>`
3. Теперь вы можете тестировать все защищенные эндпоинты

### 4. Тестирование через curl

```bash
# Получение токена
TOKEN=$(curl -s -X POST "http://localhost:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123" | jq -r '.access_token')

# Получение списка пользователей
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/users/

# Получение списка сфер
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/v1/spheres/
```

### 5. Тестирование Frontend

1. Откройте http://localhost:3000 в браузере
2. Войдите с учетными данными admin/admin123
3. Протестируйте все функции приложения

## Автоматизированное тестирование

### Запуск тестов Backend

```bash
# Войти в контейнер API
sudo docker compose exec api bash

# Запустить тесты
pytest

# Запустить тесты с подробным выводом
pytest -v

# Запустить тесты с покрытием
pytest --cov=app tests/
```

### Запуск тестов Frontend

```bash
# Войти в контейнер Frontend
sudo docker compose exec frontend bash

# Запустить тесты
npm test

# Запустить тесты в режиме watch
npm test -- --watch
```

## Тестирование производительности

### Нагрузочное тестирование API

```bash
# Установить Apache Bench
sudo apt install apache2-utils

# Тест производительности
ab -n 1000 -c 10 http://localhost:8000/docs
```

### Тестирование базы данных

```bash
# Подключение к базе данных
sudo docker compose exec db psql -U financier -d financier

# Проверка таблиц
\dt

# Проверка пользователей
SELECT * FROM users;

# Проверка сфер
SELECT * FROM spheres;
```

## Отладка

### Просмотр логов

```bash
# Логи API
sudo docker compose logs api

# Логи Frontend
sudo docker compose logs frontend

# Логи базы данных
sudo docker compose logs db

# Все логи в реальном времени
sudo docker compose logs -f
```

### Проверка состояния контейнеров

```bash
# Статус контейнеров
sudo docker compose ps

# Использование ресурсов
sudo docker stats
```

### Очистка и перезапуск

```bash
# Остановить все контейнеры
sudo docker compose down

# Удалить все данные
sudo docker compose down -v

# Пересобрать и запустить
sudo docker compose up --build -d
```

## Известные проблемы и решения

### Проблема: API не отвечает
**Решение**: Проверьте логи API и убедитесь, что база данных запущена

### Проблема: Frontend не загружается
**Решение**: Проверьте логи Frontend и убедитесь, что Vite запустился

### Проблема: Не удается войти в систему
**Решение**: Убедитесь, что пользователь admin создан и пароль правильный

### Проблема: База данных недоступна
**Решение**: Проверьте, что PostgreSQL запущен и порт 5433 свободен 