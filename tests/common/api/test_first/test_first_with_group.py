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
            [SEED_DIR / 'public.gift.json'],
            [
                {'id': 1, 'category': 'aaa', 'photo': 'aaa', 'name': 'aaa'},
                {'id': 2, 'category': 'bbb', 'photo': 'bbb', 'name': 'bbb'},
            ],
        ),
        (
            [SEED_DIR1 / 'public.gift.json'],
            [
                {'id': 1, 'category': 'ccc', 'photo': 'ccc', 'name': 'ccc'},
                {'id': 2, 'category': 'bbb', 'photo': 'bbb', 'name': 'bbb'},
            ],
        ),
    ],
)
@pytest.mark.asyncio()
async def test_first_with_group(expected_result, http_client) -> None:
    response = await http_client.get('/health')
    assert response.status_code == 200
    assert response.json() == expected_result
