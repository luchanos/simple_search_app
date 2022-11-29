from datetime import date

from starlette.requests import Request

from models import InsertDocumentModel


async def ping():
    return {"Success": True}


async def create_document(request: Request, body: InsertDocumentModel):
    db = request.app.state.db
    elastic = request.app.state.elastic
    created_date = date.today()
    async with db.pool.acquire() as connection:
        async with connection.transaction():
            QUERY = """INSERT INTO documents (rubrics, text, created_date) VALUES ($1, $2, $3) RETURNING id;"""
            document_returned_data = await connection.fetch(QUERY, body.rubrics, body.text, body.created_date)
            document_id = document_returned_data[0]["id"]
            document = {**body.dict(), "id": document_id, "created_date": created_date}
            await elastic.index(index="documents", document=document)
    return {"success": True, "document_id": document_id}
