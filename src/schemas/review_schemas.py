import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class ReviewSchema(BaseModel):
    uid: uuid.UUID
    user_uid: uuid.UUID
    book_uid: uuid.UUID
    review_text: Optional[str]
    rating: int
    created_at: datetime
    updated_at: datetime

class ReviewCreateSchema(BaseModel):
    rating: int = Field(ge=0, le=5)
    review_text: str = Field(max_length=1500)


class ReviewUpdateSchema(BaseModel):
    rating: int = Field(ge=0, le=5)
    review_text: str = Field(max_length=1500)