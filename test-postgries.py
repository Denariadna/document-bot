import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text

async def test_connection() -> None:
    # Create the async engine
    engine = create_async_engine("postgresql+asyncpg://user:password@localhost/document_bot", echo=True)
    
    # Connect to the database
    async with engine.connect() as conn:
        # Execute the query using sqlalchemy.text
        result = await conn.execute(text("SELECT 1"))
        print(result.scalar())

# Run the asynchronous function
asyncio.run(test_connection())
