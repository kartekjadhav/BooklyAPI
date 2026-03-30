from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from src.book_data import books
from src.schemas.BookSchemas import BookSchema, BookUpdateSchema, BookCreateSchema
from src.schemas.token import TokenPayLoad
from src.services.BookService import BookService
from src.db.db import get_session
from src.dependencies.bearer import AccessTokenBearer


book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()


# Get all books
@book_router.get("/", response_model=List[BookSchema], status_code=status.HTTP_200_OK)
async def get_all_books(
    session: AsyncSession = Depends(get_session), 
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    books = await book_service.get_all_books(session=session)
    return books

# Get a specific book
@book_router.get("/{book_uid}", response_model=BookSchema, status_code=status.HTTP_200_OK)
async def get_books(
    book_uid, 
    session: AsyncSession = Depends(get_session),
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    book = await book_service.get_book(book_uid=book_uid, session=session)
    if book is not None:
        return book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

# Create a book
@book_router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_data:BookCreateSchema, 
    session: AsyncSession = Depends(get_session),
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    new_book = await book_service.create_book(book_data=book_data, session=session)
    if new_book is not None:
        return new_book
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server side error")

# Update a book
@book_router.patch("/{book_uid}", response_model=BookSchema, status_code=status.HTTP_200_OK)
async def update_book(
    book_uid:str, 
    book_update_data:BookUpdateSchema, 
    session: AsyncSession = Depends(get_session),
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    updated_book = await book_service.update_book(book_uid=book_uid, book_update_data=book_update_data, session=session)
    if update_book is not None:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Server side error")

# Delete a book
@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    result = await book_service.delete_book(book_uid=book_uid, session=session)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    else:
        return {}
