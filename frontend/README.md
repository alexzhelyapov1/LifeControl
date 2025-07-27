# LifeControl Frontend

Фронтенд приложение для системы управления личными финансами LifeControl.

## Технологии

- React 18
- TypeScript
- Vite
- React Router DOM
- Axios
- Tailwind CSS

## Установка и запуск

1. Установите зависимости:
```bash
npm install
```

2. Запустите сервер разработки:
```bash
npm run dev
```

3. Откройте браузер и перейдите по адресу [http://localhost:5173](http://localhost:5173)

## Сборка для продакшена

```bash
npm run build
```

## Структура проекта

```
src/
├── components/     # Переиспользуемые компоненты
├── contexts/       # React контексты
├── pages/          # Страницы приложения
├── services/       # API сервисы
├── types/          # TypeScript типы
├── hooks/          # Кастомные хуки
└── utils/          # Утилиты
```

## API

Фронтенд настроен для работы с бэкендом на `http://localhost:8000/api/v1`.

Убедитесь, что бэкенд запущен перед использованием фронтенда.
