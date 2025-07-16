import os

# 1. Список путей до файлов (относительные пути)
# Замените этот список своими путями к файлам
# find src toolchains CMakeLists.txt .gitmodules -type f
file_paths = [
    'alembic/env.py',
    'app/api/v1/deps.py',
    'app/api/v1/endpoints/dashboard.py',
    'app/api/v1/endpoints/records.py',
    'app/api/v1/endpoints/locations.py',
    'app/api/v1/endpoints/auth.py',
    'app/api/v1/endpoints/users.py',
    'app/api/v1/endpoints/spheres.py',
    'app/api/v1/endpoints/admin.py',
    'app/api/v1/api.py',
    'app/core/security.py',
    'app/core/config.py',
    'app/models/location.py',
    'app/models/base_class.py',
    'app/models/accounting_record.py',
    'app/models/user.py',
    'app/models/sphere.py',
    'app/crud/dashboard.py',
    'app/crud/base.py',
    'app/crud/location.py',
    'app/crud/accounting_record.py',
    'app/crud/user.py',
    'app/crud/sphere.py',
    'app/schemas/dashboard.py',
    'app/schemas/location.py',
    'app/schemas/accounting_record.py',
    'app/schemas/user.py',
    'app/schemas/sphere.py',
    'app/schemas/utils.py',
    'app/schemas/token.py',
    'app/main.py',
    'app/db/base.py',
    'app/db/session.py',
    'tests/api/v1/test_login.py',
    'tests/api/v1/test_spheres.py',
    'tests/conftest.py',
    'tests/utils/user.py',
    '.env.example',
    '.gitignore',
    'alembic.ini',
    'docker-compose.override.yml',
    'docker-compose.yml',
    'Dockerfile',
    'requirements.txt',
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