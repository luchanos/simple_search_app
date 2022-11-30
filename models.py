from datetime import date
from pydantic import BaseModel, root_validator
from typing import Optional
from datetime import datetime


class InsertDocumentModel(BaseModel):
    created_date: Optional[date]
    text: str
    rubrics: list[str]

    @root_validator
    def chech_created_date(cls, values):
        if not values.get("created_date"):
            values["created_date"] = datetime.now()
        return values


class DeleteDocumentModel(BaseModel):
    document_id: int


class SearchDocumentsModel(BaseModel):
    search_query: str
