import asyncio
import os
from fastapi.testclient import TestClient

import pytest
import asyncpg
from elasticsearch import AsyncElasticsearch, NotFoundError

import settings
from main import app
from scripts.index_creation import MAPPING_FOR_INDEX


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
def create_database_and_run_migrations():
    print("Running migrations...")
    os.system(f"yoyo apply --database postgresql://postgres:postgres@0.0.0.0:5432/postgres ../migrations -b")
    print("Migrations completed successfully.")


@pytest.fixture(scope="session")
async def test_db():
    pool = await asyncpg.create_pool("postgresql://postgres:postgres@0.0.0.0:5432/postgres")
    yield pool
    pool.close()


@pytest.fixture(scope="session")
async def test_client():
    with TestClient(app) as client:
        yield client


@pytest.fixture(scope="function")
async def test_elastic():
    test_elastic = AsyncElasticsearch(settings.TEST_ELASTIC_URL)
    yield test_elastic


@pytest.fixture(scope="function", autouse=True)
async def clean_tables(test_db):
    """Clean data in all tables before running test function"""
    async with test_db.acquire() as connection:
        async with connection.transaction():
            await connection.execute("""TRUNCATE TABLE documents;""")


@pytest.fixture(scope="function", autouse=True)
async def clean_indexes(test_elastic):
    """Clean data in all indexes before running test function"""
    try:
        await test_elastic.indices.delete(index="documents")
    except NotFoundError:
        print("Index for deleting not found")
    await test_elastic.indices.create(index="documents", mappings=MAPPING_FOR_INDEX)
