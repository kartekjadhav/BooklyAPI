import uuid
from datetime import datetime, timezone, date
from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg

class Books(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))

    def __repr__(self):
        return f"<Book {self.title}>"