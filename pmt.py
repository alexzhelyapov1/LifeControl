import os

# 1. Список путей до файлов (относительные пути)
# Замените этот список своими путями к файлам
# find src toolchains CMakeLists.txt .gitmodules -type f
file_paths = [
    'backend/Dockerfile',
    'backend/pytest.ini',
    'backend/alembic.ini',
    'backend/requirements.txt',
    'backend/alembic/env.py',
    'backend/tests/api/v1/test_spheres.py',
    'backend/tests/api/v1/test_auth.py',
    'backend/tests/conftest.py',
    'backend/tests/utils/user.py',
    'backend/app/api/v1/deps.py',
    'backend/app/api/v1/endpoints/dashboard.py',
    'backend/app/api/v1/endpoints/records.py',
    'backend/app/api/v1/endpoints/locations.py',
    'backend/app/api/v1/endpoints/auth.py',
    'backend/app/api/v1/endpoints/users.py',
    'backend/app/api/v1/endpoints/spheres.py',
    'backend/app/api/v1/endpoints/admin.py',
    'backend/app/api/v1/api.py',
    'backend/app/core/security.py',
    'backend/app/core/config.py',
    'backend/app/models/location.py',
    'backend/app/models/base_class.py',
    'backend/app/models/accounting_record.py',
    'backend/app/models/user.py',
    'backend/app/models/sphere.py',
    'backend/app/crud/dashboard.py',
    'backend/app/crud/base.py',
    'backend/app/crud/location.py',
    'backend/app/crud/accounting_record.py',
    'backend/app/crud/user.py',
    'backend/app/crud/sphere.py',
    'backend/app/schemas/dashboard.py',
    'backend/app/schemas/location.py',
    'backend/app/schemas/accounting_record.py',
    'backend/app/schemas/user.py',
    'backend/app/schemas/sphere.py',
    'backend/app/schemas/utils.py',
    'backend/app/schemas/token.py',
    'backend/app/main.py',
    'backend/app/db/base.py',
    'backend/app/db/session.py',
    '.env',
    '.env.example',
    '.gitignore',
    'docker-compose.override.yml',
    'docker-compose.test.yml',
    'docker-compose.yml',
    'run-tests.sh',
]

# Имя выходного файла
output_filename = "context.txt"

# Кодировка для чтения и записи файлов (рекомендуется UTF-8)
encoding = 'utf-8'

# print(f"Начинаю объединение файлов в {output_filename}...")

# 2. Открываем выходной файл для записи ('w' - перезапишет файл, если он существует)
try:
    with open(output_filename, 'w', encoding=encoding) as outfile:
        # Проходим по каждому пути в списке
        for file_path in file_paths:
            # print(f"Обработка: {file_path}")
            # Записываем разделитель и путь к файлу
            outfile.write(f"{'-' * 29}\n--- File: {file_path} ---\n{'-' * 29}\n")

            # Проверяем, существует ли файл
            if os.path.exists(file_path):
                try:
                    # Открываем текущий файл для чтения
                    with open(file_path, 'r', encoding=encoding) as infile:
                        # Читаем все содержимое файла
                        content = infile.read()
                        # Записываем содержимое в выходной файл
                        outfile.write(content)
                        # Добавляем перевод строки в конце содержимого файла, если его нет
                        if not content.endswith('\n'):
                            outfile.write('\n')

                except FileNotFoundError:
                    # Эта ветка не должна сработать из-за os.path.exists,
                    # но оставим на всякий случай
                    warning_msg = "[!] ОШИБКА: Файл не найден (хотя os.path.exists его видел?).\n"
                    print(f"  {warning_msg.strip()}")
                    outfile.write(warning_msg)
                except UnicodeDecodeError:
                    warning_msg = f"[!] ОШИБКА: Не удалось прочитать файл {file_path} с кодировкой {encoding}. Попробуйте другую кодировку или проверьте файл.\n"
                    print(f"  {warning_msg.strip()}")
                    outfile.write(warning_msg)
                except Exception as e:
                    # Ловим другие возможные ошибки при чтении файла
                    error_msg = f"[!] ОШИБКА: Не удалось прочитать файл {file_path}. Причина: {e}\n"
                    print(f"  {error_msg.strip()}")
                    outfile.write(error_msg)
            else:
                # Если файл не найден
                not_found_msg = "[!] Файл не найден по указанному пути.\n"
                print(f"  Предупреждение: Файл {file_path} не найден, пропускаю.")
                outfile.write(not_found_msg)

            # Добавляем пару пустых строк для лучшего разделения между файлами
            outfile.write("\n\n")

    # print("-" * 30)
    # print(f"Готово! Все найденные файлы были объединены в файл: {output_filename}")

except IOError as e:
    print(f"Ошибка при открытии или записи в выходной файл {output_filename}: {e}")
except Exception as e:
    print(f"Произошла непредвиденная ошибка: {e}")