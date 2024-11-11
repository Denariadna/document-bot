FROM python:3.12-slim

WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY ./src /app/src

CMD ["poetry", "run", "python", "src/main.py"]
