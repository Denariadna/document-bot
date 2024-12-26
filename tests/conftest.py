import aiohttp
import httpx
from unittest.mock import AsyncMock, MagicMock
import pytest
import pytest_asyncio
from collections import deque
from asgi_lifespan import LifespanManager
from fastapi import FastAPI

from tests.mocking.rabbit import MockChannel, MockChannelPool, MockExchange, MockQueue
from scripts.migrate import migrate
from src.app import create_app
from src.storage import minio_client, rabbit


@pytest.fixture(scope="session")
def monkeypatch():
    """Создает фикстуру monkeypatch на уровне сессии."""
    from _pytest.monkeypatch import MonkeyPatch
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _init_db() -> aiohttp.ClientSession:
    """Инициализация базы данных."""
    await migrate()
    yield
    # TODO: добавить удаление базы данных.


@pytest.fixture(scope="session")
def app() -> FastAPI:
    return create_app()


@pytest_asyncio.fixture(scope="session")
async def http_client(app: FastAPI) -> httpx.AsyncClient:
    async with LifespanManager(app):
        async with httpx.AsyncClient(app=app, base_url="http://localhost") as client:
            yield client


@pytest.fixture(scope="session", autouse=True)
def mock_rabbit_dependencies(monkeypatch: pytest.MonkeyPatch):
    """Мокаем RabbitMQ зависимости."""
    # Создаем мок-канал и мок-обменник
    mock_queue = MockQueue(queue=deque())
    mock_exchange = MockExchange()
    mock_channel = MockChannel(queue=mock_queue, exchange=mock_exchange)
    mock_channel_pool = MockChannelPool(channel=mock_channel)

    # Мокаем метод acquire, чтобы возвращать mock_channel_pool
    monkeypatch.setattr(rabbit, "channel_pool", mock_channel_pool)

    yield


@pytest.fixture(scope="session", autouse=True)
def mock_minio_dependencies(monkeypatch: pytest.MonkeyPatch):
    """Мокаем MinIO зависимости."""
    monkeypatch.setattr(minio_client, "create_bucket", AsyncMock())
    monkeypatch.setattr(minio_client, "minio_client", MagicMock())
    yield
