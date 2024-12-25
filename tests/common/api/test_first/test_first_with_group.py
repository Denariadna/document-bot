from pathlib import Path

import pytest

BASE_DIR = Path(__file__).parent
SEED_DIR = BASE_DIR / 'seeds'
SEED_DIR1 = BASE_DIR / 'seeds1'


@pytest.mark.usefixtures('_load_seeds')
@pytest.mark.parametrize(
    ('seeds', 'expected_result'),
    [
        (
            [SEED_DIR / 'public.file_records.json'],
            [
                {"user_id": 1, "action": "upload_file", "file_name": "aaa.pdf"},
                {"user_id": 2, "action": "upload_file", "file_name": "bbb.pdf"}
            ],
        ),
        (
            [SEED_DIR1 / 'public.file_records.json'],
            [
                {"user_id": 1, "action": "upload_file", "file_name": "aaa.pdf"},
                {"user_id": 2, "action": "upload_file", "file_name": "bbb.pdf"}
            ],
        ),
    ],
)
@pytest.mark.asyncio()
async def test_first_with_group(expected_result, http_client) -> None:
    response = await http_client.get('/health')
    assert response.status_code == 200
    assert response.json() == expected_result
