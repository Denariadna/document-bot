from typing import List


class MockMinioClient:
    def __init__(self):
        self.buckets: List[str] = []

    async def create_bucket(self, bucket_name: str) -> None:
        if bucket_name in self.buckets:
            raise ValueError(f"Bucket '{bucket_name}' already exists")
        self.buckets.append(bucket_name)
        print(f"Bucket '{bucket_name}' created")

    async def list_buckets(self) -> List[str]:
        """
        Возвращает список созданных бакетов.
        """
        return self.buckets
