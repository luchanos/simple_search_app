from pydantic import BaseModel, Extra
from datetime import datetime


class InsertDocumentModel(BaseModel, extra=Extra.forbid):
    created_date: datetime
    text: str
    rubrics: list[str]


class DeleteDocumentModel(BaseModel):
    document_id: int


class SearchDocumentsModel(BaseModel):
    search_query: str
