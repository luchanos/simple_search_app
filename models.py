from datetime import datetime
from pydantic import BaseModel, root_validator, Extra
from typing import Optional
from datetime import datetime, date


class InsertDocumentModel(BaseModel, extra=Extra.forbid):
    created_date: datetime
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
