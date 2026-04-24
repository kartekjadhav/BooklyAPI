from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import Response
from typing import List, Annotated
from sqlmodel.ext.asyncio.session import AsyncSession
from src.book_data import books
from src.schemas.BookSchemas import BookSchema, BookUpdateSchema, BookCreateSchema, BookWithReviewsSchema
from src.schemas.token import TokenPayLoad
from src.services.book_service import BookService
from src.db.db import get_session
from src.dependencies.bearer import AccessTokenBearer
from src.dependencies.role_checker import RoleChecker



book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(allowed_roles=["user", "admin"]))

# Get all books
@book_router.get("/", response_model=List[BookSchema], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_all_books(
    session: AsyncSession = Depends(get_session), 
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    books = await book_service.get_all_books(session=session)
    return books

# Get a specific book
@book_router.get("/{book_uid}", response_model=BookWithReviewsSchema, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_books(
    book_uid, 
    session: AsyncSession = Depends(get_session),
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    book = await book_service.get_book(book_uid=book_uid, session=session)
    return book

# Create a book
@book_router.post("/", response_model=BookSchema, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def create_book(
    book_data:BookCreateSchema, 
    session: AsyncSession = Depends(get_session),
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    new_book = await book_service.create_book(user_uid=tokenData["user"]["uid"], book_data=book_data, session=session)
    if new_book is not None:
        return new_book
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Update a book
@book_router.patch("/{book_uid}", response_model=BookSchema, status_code=status.HTTP_200_OK, dependencies=[role_checker])
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
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Delete a book
@book_router.delete("/{book_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_book(
    book_uid: str, 
    session: AsyncSession = Depends(get_session),
    tokenData: TokenPayLoad = Depends(access_token_bearer)
):
    await book_service.delete_book(book_uid=book_uid, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
