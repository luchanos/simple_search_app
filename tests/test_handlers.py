import datetime

from main import app
from fastapi.testclient import TestClient


async def create_document(test_db, test_elastic, document_id, rubrics, text, created_date):
    """Function for custom document creation"""
    async with test_db.acquire() as connection:
        async with connection.transaction():
            document_returned_data = await connection.fetch(
                """INSERT INTO documents (id, rubrics, text, created_date) VALUES ($1, $2, $3, $4) RETURNING id;""",
                document_id,
                rubrics,
                text,
                created_date)
            document_id = document_returned_data[0]["id"]
            document = {"id": document_id, "rubrics": rubrics, "created_date": created_date, "text": text}
            await test_elastic.index(index="documents", document=document)
    return document_id


async def test_create_document(test_db, test_elastic):
    text = "sample text"
    rubrics = ["python", "programming", "backend"]
    date_string = "2032-11-23"
    time_string = "10:20:30"
    created_date_string = f"{date_string}T{time_string}"
    document_data = {
        "text": text,
        "rubrics": rubrics,
        "created_date": created_date_string
    }
    with TestClient(app) as client:
        res = client.post("/create_document", json=document_data)
        resp = res.json()
        assert res.status_code == 200
        assert resp["success"]
        document_id = resp["document_id"]

    async with test_db.acquire() as connection:
        document_returned_data = await connection.fetch("""SELECT * FROM documents WHERE id = $1;""", document_id)
        assert len(document_returned_data) == 1
        returned_document = document_returned_data[0]
        assert returned_document["id"] == document_id
        assert returned_document["rubrics"] == rubrics
        assert str(returned_document["created_date"]) == f"{date_string} {time_string}"
        assert returned_document["text"] == text

    documents_from_elastic = await test_elastic.search(index="documents", query={"match": {"Id": document_id}})
    assert len(documents_from_elastic.body["hits"]["hits"]) == 1
    document_from_elastic = documents_from_elastic["hits"]["hits"][0]["_source"]
    assert document_from_elastic["text"] == text
    assert document_from_elastic["Id"] == document_id


async def test_delete_document(test_db, test_elastic):
    text = "sample text"
    rubrics = ["python", "programming", "backend"]
    year, month, day, hour, minute, second = 2032, 11, 23, 10, 20, 30
    date_string = f"{year}-{month}-{day}"
    time_string = f"{hour}:{minute}:{second}"
    created_date_string = f"{date_string} {time_string}"
    date_string = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    document_data = {
        "text": text,
        "rubrics": rubrics,
        "created_date": date_string
    }

    document_id = await create_document(test_db, test_elastic, document_id=1, **document_data)
    with TestClient(app) as client:
        res = client.delete(f"/delete_document?document_id={document_id}")
        resp = res.json()
        assert res.status_code == 200
        assert resp["success"]
        document_id = resp["document_id"]

    async with test_db.acquire() as connection:
        document_returned_data = await connection.fetch("""SELECT * FROM documents WHERE id = $1;""", document_id)
        assert len(document_returned_data) == 1
        returned_document = document_returned_data[0]
        assert returned_document["id"] == document_id
        assert returned_document["rubrics"] == rubrics
        assert str(returned_document["created_date"]) == created_date_string
        assert returned_document["text"] == text
        assert returned_document["is_deleted"]

    documents_from_elastic = await test_elastic.search(index="documents", query={"match": {"Id": document_id}})
    assert len(documents_from_elastic.body["hits"]["hits"]) == 0
