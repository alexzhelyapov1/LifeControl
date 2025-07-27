# LifeControl - Система управления финансами

## Описание

LifeControl - это веб-приложение для управления личными финансами, построенное на современном стеке технологий:

- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: React + Vite + TypeScript
- **База данных**: PostgreSQL
- **Контейнеризация**: Docker + Docker Compose

## Быстрый запуск

### Автоматический запуск

Для быстрого запуска всего приложения выполните:

```bash
./start.sh
```

Этот скрипт:
- Создаст файл `.env` с необходимыми переменными окружения
- Запустит все сервисы (база данных, API, фронтенд)
- Создаст пользователя admin с паролем admin123
- Проверит статус всех сервисов

### Ручной запуск

#### 1. Создание .env файла

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

#### 2. Запуск приложения

```bash
# Остановить существующие контейнеры
sudo docker compose down

# Запустить все сервисы
sudo docker compose up --build -d

# Проверить статус
sudo docker compose ps
```

## Доступ к приложению

После успешного запуска приложение будет доступно по следующим адресам:

- **Frontend**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc
- **Database**: localhost:5433 (PostgreSQL)

## Тестовые данные

При первом запуске автоматически создается пользователь admin:

- **Логин**: admin
- **Пароль**: admin123
- **Роль**: Администратор

## Управление контейнерами

### Просмотр логов

```bash
# Все сервисы
sudo docker compose logs

# Конкретный сервис
sudo docker compose logs api
sudo docker compose logs frontend
sudo docker compose logs db
```

### Остановка приложения

```bash
sudo docker compose down
```

### Перезапуск с пересборкой

```bash
sudo docker compose down
sudo docker compose up --build -d
```

## Структура проекта

```
LifeControl/
├── backend/                 # Backend приложение (FastAPI)
│   ├── app/
│   │   ├── api/            # API эндпоинты
│   │   ├── core/           # Конфигурация и утилиты
│   │   ├── crud/           # CRUD операции
│   │   ├── db/             # Настройки базы данных
│   │   ├── models/         # SQLAlchemy модели
│   │   └── schemas/        # Pydantic схемы
│   ├── alembic/            # Миграции базы данных
│   ├── requirements.txt     # Python зависимости
│   └── Dockerfile          # Docker образ для backend
├── frontend/               # Frontend приложение (React)
│   ├── src/                # Исходный код
│   ├── package.json        # Node.js зависимости
│   └── Dockerfile          # Docker образ для frontend
├── docker-compose.yml      # Docker Compose конфигурация
├── start.sh               # Скрипт автоматического запуска
└── README.md              # Документация
```

## API Endpoints

### Аутентификация
- `POST /api/v1/auth/token` - Получение JWT токена

### Пользователи
- `GET /api/v1/users/` - Список пользователей
- `POST /api/v1/users/` - Создание пользователя
- `GET /api/v1/users/{user_id}` - Получение пользователя
- `PUT /api/v1/users/{user_id}` - Обновление пользователя
- `DELETE /api/v1/users/{user_id}` - Удаление пользователя

### Сферы
- `GET /api/v1/spheres/` - Список сфер
- `POST /api/v1/spheres/` - Создание сферы
- `GET /api/v1/spheres/{sphere_id}` - Получение сферы
- `PUT /api/v1/spheres/{sphere_id}` - Обновление сферы
- `DELETE /api/v1/spheres/{sphere_id}` - Удаление сферы

### Локации
- `GET /api/v1/locations/` - Список локаций
- `POST /api/v1/locations/` - Создание локации
- `GET /api/v1/locations/{location_id}` - Получение локации
- `PUT /api/v1/locations/{location_id}` - Обновление локации
- `DELETE /api/v1/locations/{location_id}` - Удаление локации

### Учетные записи
- `GET /api/v1/accounting-records/` - Список записей
- `POST /api/v1/accounting-records/` - Создание записи
- `GET /api/v1/accounting-records/{record_id}` - Получение записи
- `PUT /api/v1/accounting-records/{record_id}` - Обновление записи
- `DELETE /api/v1/accounting-records/{record_id}` - Удаление записи

## Разработка

### Локальная разработка

Для разработки без Docker:

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate     # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Миграции базы данных

```bash
# Создание новой миграции
cd backend
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграции
alembic downgrade -1
```

## Тестирование

```bash
# Backend тесты
cd backend
pytest

# Frontend тесты
cd frontend
npm test
```

## Troubleshooting

### Проблемы с Docker

1. **Docker не запущен**:
   ```bash
   sudo systemctl start docker
   ```

2. **Порт занят**:
   - Измените порты в `docker-compose.yml`
   - Или остановите процессы, использующие порты

3. **Проблемы с правами**:
   ```bash
   sudo usermod -aG docker $USER
   # Перезапустите сессию
   ```

### Проблемы с базой данных

1. **Очистка данных**:
   ```bash
   sudo docker compose down -v
   sudo docker compose up --build -d
   ```

2. **Проверка подключения**:
   ```bash
   sudo docker compose exec db psql -U financier -d financier
   ```

## Лицензия

MIT License