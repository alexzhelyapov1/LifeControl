# 1. Очистка (на всякий случай)
flutter clean

# 2. Удаление файла блокировки зависимостей (чтобы гарантировать свежие версии)
rm -f pubspec.lock

# 3. Получение всех зависимостей заново
flutter pub get

# 4. Повторный запуск генерации кода
dart run build_runner build --delete-conflicting-outputs