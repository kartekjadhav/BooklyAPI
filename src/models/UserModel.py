import uuid
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg

if TYPE_CHECKING:
    from .BooksModel import Books

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

    def __repr__(self):
        return f"<User {self.username}>"