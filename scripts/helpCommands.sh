# Виртуальный окружение
python3 -m venv venv
source venv/bin/activate
# deactivate
# rm -rf venv

# Зависимости
python3 -m poetry install # Установка зависимостей из poetry.lock
python3 -m poetry lock # Заполнение poetry.lock
# poetry install

# Запуск Docker
docker compose up --build -d
# docker kill $(docker ps -a -q)

# Запустить app.py (bot_polling)
python3 -m src.app

# Удалять мусор
# sudo find . -name '__pycache__' -type d -exec rm -rf {} +

# вывести древо проекта
# tree -I '.vscode|venv|.mypy_cache|__pycache__'

# Миграции
# alembic init alembic
# add sqlalchemy.url = postgresql://postgres:mypassword@localhost:5432/mydatabase
# alembic revision --autogenerate -m "init"
# alembic/versions/<revision_id>_init.py
# alembic upgrade head