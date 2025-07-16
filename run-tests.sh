#!/bin/bash
set -e

# Этот скрипт запускает тесты в изолированном Docker-окружении.

# Запуск контейнеров в фоновом режиме
docker-compose -f docker-compose.test.yml up -d --build

# Выполнение pytest внутри контейнера api_test
# --exit-code-from api_test дождется завершения тестов и вернет их код выхода.
docker-compose -f docker-compose.test.yml run --rm api_test pytest

# Сохраняем код выхода тестов
EXIT_CODE=$?

# Остановка и удаление контейнеров
docker-compose -f docker-compose.test.yml down

# Выход с кодом, который вернули тесты
exit $EXIT_CODE