from pydantic import BaseModel, Field, EmailStr
import uuid
from datetime import datetime

class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    password: str = Field(min_length=6, max_length=30)
    email: EmailStr = Field(max_length=100)


class UsersSchema(BaseModel):
    uid: uuid.UUID
    username: str
    password_hash: str = Field(exclude=True)
    first_name: str
    last_name: str
    email: str 
    verified: bool
    created_at: datetime
    updated_at: datetime

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(max_length=100)
    password: str = Field(min_length=6, max_length=30)