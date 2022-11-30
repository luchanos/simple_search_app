from elasticsearch import AsyncElasticsearch
from starlette.requests import Request

from models import InsertDocumentModel


async def ping():
    return {"Success": True}


async def create_document(request: Request, body: InsertDocumentModel):
    db = request.app.state.db
    elastic = request.app.state.elastic
    async with db.pool.acquire() as connection:
        async with connection.transaction():

            QUERY = """INSERT INTO documents (rubrics, text, created_date)
                       VALUES ($1, $2, $3)
                       ON CONFLICT(id)
                       DO UPDATE SET
                       rubrics=$1,
                       text=$2,
                       created_date=$3,
                       is_deleted=false
                       RETURNING id;"""
            document_returned_data = await connection.fetch(QUERY, body.rubrics, body.text, body.created_date)
            document_id = document_returned_data[0]["id"]
            document = {**body.dict(), "Id": document_id}
            await elastic.index(index="documents", document=document, refresh="wait_for")
    return {"success": True, "document_id": document_id}


async def delete_document(request: Request, document_id: int):
    db = request.app.state.db
    elastic: AsyncElasticsearch = request.app.state.elastic
    async with db.pool.acquire() as connection:
        async with connection.transaction():
            QUERY = """UPDATE documents SET is_deleted=true WHERE id=$1 RETURNING id;"""
            document_returned_data = await connection.fetch(QUERY, document_id)
            document_id = document_returned_data[0]["id"]
            await elastic.delete_by_query(index="documents", query={"match": {"Id": document_id}})
            await elastic.indices.refresh(index="documents")
    return {"success": True, "document_id": document_id}
