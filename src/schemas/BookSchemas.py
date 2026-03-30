from pydantic import BaseModel
import uuid
from datetime import datetime, date


class BookSchema(BaseModel):
    uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookCreateSchema(BaseModel):
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str

class BookUpdateSchema(BaseModel):
    author: str | None = None
    publisher: str | None = None
    publish_date: date | None = None
    page_count: int | None = None
    language: str | None = None