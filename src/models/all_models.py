import uuid
from typing import List, Optional
from datetime import datetime, timezone, date
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg


# Users Model
class Users(SQLModel, table=True):
    __tablename__ = "users"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    username: str = Field(min_length=3, max_length=30)
    password_hash: str = Field(exclude=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: str = Field(unique=True)
    role: str = Field(sa_column=Column(pg.VARCHAR, nullable=False, server_default="user"))
    verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True)))
    updated_at: datetime = Field(default_factory= lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True)))
    books: Optional[List["Books"]] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'})
    reviews: Optional[List["Reviews"]] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'})

    def __repr__(self):
        return f"<User {self.username}>"
    


# Books Model
class Books(SQLModel, table=True):
    __tablename__ = "books"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    author: str
    publisher: str
    publish_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    user: Optional["Users"] = Relationship(back_populates="books")
    reviews: Optional[List["Reviews"]] = Relationship(back_populates="book", sa_relationship_kwargs={'lazy': 'selectin'})

    def __repr__(self):
        return f"<Book {self.title}>"
    

class Reviews(SQLModel, table=True):
    __tablename__ = "reviews"

    uid: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, nullable=False)
    user_uid: uuid.UUID = Field(foreign_key="users.uid", index=True)
    book_uid: uuid.UUID = Field(foreign_key="books.uid", index=True)
    review_text: Optional[str] = Field(default=None, sa_column=Column(pg.VARCHAR(1500)))
    rating: int = Field(default=0, le=5, ge=0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(tz=timezone.utc), sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False))
    user: Optional["Users"] = Relationship(back_populates="reviews")
    book: Optional["Books"] = Relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_id}, by user {self.user_id}>"