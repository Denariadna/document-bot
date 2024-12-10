# Виртуальный окружение
python3 -m venv .venv
source .venv/bin/activate
# deactivate
# rm -rf .venv

# Зависимости
python3 -m pip install poetry # Установка poetry
python3 -m poetry install # Установка зависимостей из poetry.lock
python3 -m poetry lock # Заполнение poetry.lock
# poetry install

# Запуск Docker
docker compose up --build -d
# docker kill $(docker ps -a -q)

# docker compose down
# docker compose build --no-cache
# docker compose up

# Запустить app.py (bot_polling)
python3 -m src.app
PYTHONPATH=. python3 -m src.app


# Запустить app.py (bot_webhook)
python3 -m uvicorn src.app:create_app --factory --host 0.0.0.0 --port 8000
# command: poetry run uvicorn src.app:create_app --factory --host 0.0.0.0 --port 8001 --workers=1


# Удалять мусор
# sudo find . -name '__pycache__' -type d -exec rm -rf {} +

# Скачать модуль в poetry
# python3 -m poetry add <module_name>

# вывести древо проекта
# tree -I '.vscode|.venv|.mypy_cache|__pycache__'

# find . -type f \
# ! -path './.vscode/*' \
#     ! -path './node_modules/*' \
#     ! -path './.venv/*' \
#     ! -path './.mypy_cache/*' \
#     ! -path './pycache/*' \
#     ! -path './src/storage/__pycache__/*.cpython-312.pyc' \
#     ! -name '*.cpython-312.pyc' \
#     ! -path '*/__pycache__/*.pyc' \
#     ! -path './.git/*' \
#     ! -path './poetry.lock' \
#     -exec echo "Opening file: {}" \; -exec cat {} \;

# Миграции
# alembic init alembic
# add sqlalchemy.url = postgresql://postgres:mypassword@localhost:5432/mydatabase
# alembic revision --autogenerate -m "init"
# alembic/versions/<revision_id>_init.py
# alembic upgrade head
