from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session 
from src.schemas.review_schemas import ReviewCreateSchema, ReviewSchema
from .user_service import UserService
from .book_service import BookService
from src.models.all_models import Reviews


user_service = UserService()
book_service = BookService()

class ReviewServices():
    async def add_book_review(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateSchema,
        session: AsyncSession
    ) -> Reviews:
        user = await user_service.get_user_by_email(email=user_email, session=session)
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
        
        book = await book_service.get_book(book_uid=book_uid, session=session)
        if book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Book not found')

        review_data_dict = review_data.model_dump()

        new_review = Reviews(**review_data_dict)
        new_review.book = book
        new_review.user = user

        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
        return new_review