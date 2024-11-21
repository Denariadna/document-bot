# Виртуальный окружение
python3 -m venv venv
source venv/bin/activate
# deactivate
# rm -rf venv

# Зависимости
python3 -m poetry install # Установка зависимостей из poetry.lock
python3 -m poetry lock # Заполнение poetry.lock
# poetry install

# Запуск
docker compose up --build -d
# docker kill $(docker ps -a -q)

# Удалять мусор
# sudo find . -name '__pycache__' -type d -exec rm -rf {} +

# Миграции
# alembic init alembic
# add sqlalchemy.url = postgresql://postgres:mypassword@localhost:5432/mydatabase
# alembic revision --autogenerate -m "init"
# alembic/versions/<revision_id>_init.py
# alembic upgrade head