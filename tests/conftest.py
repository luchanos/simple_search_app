import asyncio
import os

import pytest
from httpx import AsyncClient
from main import app
from fastapi.testclient import TestClient
from subprocess import Popen, PIPE


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
async def db():
    yield app.state.db


@pytest.fixture(scope="function", autouse=True)
async def clean_tables():
    """Clean data in all collections before running test function"""
    c = 1
