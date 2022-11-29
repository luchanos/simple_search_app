from main import app
from fastapi.testclient import TestClient


async def test_create_document(db):
    document_data = {
        "text": "sample text",
        "rubrics": ["python", "programming", "backend"],
        "created_date": "2022-01-01"
    }

    with TestClient(app) as client:
        res = client.post("/create_document", json=document_data)
        c = 1