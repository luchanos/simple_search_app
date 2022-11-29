from datetime import date
from pydantic import BaseModel
from typing import Optional


class InsertDocumentModel(BaseModel):
    created_date: Optional[date]
    text: str
    rubrics: list[str]


class SearchDocumentsModel(BaseModel):
    search_query: str
