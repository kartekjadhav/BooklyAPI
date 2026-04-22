from pydantic import BaseModel
import uuid
from datetime import datetime, date
from typing import List
from .review_schemas import ReviewSchema


class BookSchema(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str
    created_at: datetime
    updated_at: datetime

class BookWithReviewsSchema(BookSchema):
    reviews: List[ReviewSchema]

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