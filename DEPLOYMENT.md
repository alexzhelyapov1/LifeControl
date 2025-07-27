# LifeControl - Инструкция по развертыванию

## Быстрый запуск

Для быстрого запуска всего приложения выполните:

```bash
./start.sh
```

Этот скрипт:
- Создаст файл `.env` с необходимыми переменными окружения
- Запустит все сервисы (база данных, API, фронтенд)
- Создаст пользователя admin с паролем admin
- Проверит статус всех сервисов

## Ручной запуск

### 1. Создание .env файла

Создайте файл `.env` в корне проекта:

```bash
cat > .env << EOF
# Database Configuration
POSTGRES_SERVER=db
POSTGRES_USER=financier
POSTGRES_PASSWORD=financier_password
POSTGRES_DB=financier
POSTGRES_PORT=5432

# JWT Settings
SECRET_KEY=your-secret-key-here-change-in-production-123456789
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Frontend Configuration
VITE_API_BASE_URL=http://localhost:8000
EOF
```

### 2. Запуск приложения

```bash
docker-compose up --build -d
```

### 3. Проверка статуса

```bash
docker-compose ps
```

## Доступные сервисы

После успешного запуска будут доступны:

- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Database**: localhost:5432

## Учетные данные для тестирования

- **Login**: admin
- **Password**: admin

## Управление приложением

### Остановка
```bash
docker-compose down
```

### Просмотр логов
```bash
docker-compose logs -f
```

### Просмотр логов конкретного сервиса
```bash
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f db
```

### Перезапуск с пересборкой
```bash
docker-compose down
docker-compose up --build -d
```

## Структура проекта

```
LifeControl/
├── backend/                 # FastAPI бэкенд
│   ├── app/                # Основной код приложения
│   ├── alembic/            # Миграции базы данных
│   ├── init_db.py          # Скрипт инициализации БД
│   └── Dockerfile          # Docker образ для бэкенда
├── frontend/               # React фронтенд
│   ├── src/                # Исходный код
│   └── Dockerfile          # Docker образ для фронтенда
├── docker-compose.yml      # Конфигурация Docker Compose
├── start.sh               # Скрипт автоматического запуска
└── .env                   # Переменные окружения
```

## Технологический стек

### Backend
- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM
- **PostgreSQL** - база данных
- **Alembic** - миграции БД
- **JWT** - аутентификация

### Frontend
- **React** - UI библиотека
- **TypeScript** - типизация
- **Vite** - сборщик
- **Tailwind CSS** - стилизация

### DevOps
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация контейнеров

## Устранение неполадок

### Проблема: Контейнеры не запускаются
```bash
# Проверьте логи
docker-compose logs

# Пересоберите образы
docker-compose down
docker-compose up --build -d
```

### Проблема: База данных не подключается
```bash
# Проверьте переменные окружения
cat .env

# Перезапустите только базу данных
docker-compose restart db
```

### Проблема: API не отвечает
```bash
# Проверьте логи API
docker-compose logs api

# Проверьте миграции
docker-compose exec api alembic current
```

### Проблема: Frontend не загружается
```bash
# Проверьте логи фронтенда
docker-compose logs frontend

# Проверьте конфигурацию Vite
docker-compose exec frontend cat vite.config.ts
```

## Разработка

### Добавление новых миграций
```bash
docker-compose exec api alembic revision --autogenerate -m "Description"
docker-compose exec api alembic upgrade head
```

### Установка новых зависимостей
```bash
# Backend
docker-compose exec api pip install new-package
docker-compose exec api pip freeze > requirements.txt

# Frontend
docker-compose exec frontend npm install new-package
```

### Hot reload
Все изменения в коде автоматически перезагружаются благодаря volume mounts в docker-compose.yml. 