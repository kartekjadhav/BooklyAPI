from datetime import datetime, timezone
from typing import List
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from src.schemas.BookSchemas import BookSchema, BookCreateSchema, BookUpdateSchema
from src.models.BooksModel import Books


class BookService:
    # Get all books
    async def get_all_books(self, session: AsyncSession) -> List[BookSchema]:
        statement = select(Books).order_by(desc(Books.created_at))
        result = await session.exec(statement)
        return result.all()

    # Get a book
    async def get_book(self, book_uid: str, session: AsyncSession) -> BookSchema:
        statement = select(Books).where(Books.uid == book_uid)
        result = await session.exec(statement)
        book = result.first()
        return book if book is not None else None

    # Create book
    async def create_book(self, book_data: BookCreateSchema, session: AsyncSession) -> BookSchema:
        book_data_dict = book_data.model_dump()
        new_book = Books(**book_data_dict)
        session.add(new_book)
        await session.commit()
        return new_book

    # Update book
    async def update_book(self, book_uid: str, book_update_data: BookUpdateSchema, session: AsyncSession) -> BookSchema:
        book_to_update = await self.get_book(book_uid, session)
        if book_to_update is not None:
            book_data_dict = book_update_data.model_dump(exclude_unset=True)
            for key, value in book_data_dict.items():
                setattr(book_to_update, key, value)
            book_to_update.updated_at = datetime.now(timezone.utc)

            session.add(book_to_update)
            await session.commit()
            return book_to_update
        else:
            return None

    # Delete book
    async def delete_book(self, book_uid: str, session: AsyncSession) -> None:
        book_to_delete = await self.get_book(book_uid, session)
        if book_to_delete is not None:
            await session.delete(book_to_delete)
            await session.commit()
            return {}
        else:
            return None