from typing import List
from datetime import datetime, timezone
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.db import get_session 
from src.schemas.review_schemas import ReviewCreateSchema, ReviewSchema, ReviewUpdateSchema
from .user_service import UserService
from .book_service import BookService
from src.models.all_models import Reviews
from src.errors.errors import (UserNotFound, BookNotFound, ReviewNotFound)

user_service = UserService()
book_service = BookService()

class ReviewServices():
    async def get_all_reviews(self, session: AsyncSession) -> List[Reviews]:
        statement = select(Reviews).order_by(Reviews.created_at)
        result = await session.exec(statement=statement)
        all_reviews = result.all()
        return all_reviews

    async def get_a_review(self, review_uid:str, session: AsyncSession) -> Reviews:
        statement = select(Reviews).where(Reviews.uid == review_uid)
        result = await session.exec(statement=statement)
        review = result.first()
        if review:
            return review
        raise ReviewNotFound()

    async def add_book_review(
        self,
        user_email: str,
        book_uid: str,
        review_data: ReviewCreateSchema,
        session: AsyncSession
    ) -> Reviews:
        user = await user_service.get_user_by_email(email=user_email, session=session)
        if user is None:
            raise UserNotFound()
        
        book = await book_service.get_book(book_uid=book_uid, session=session)
        if book is None:
            raise BookNotFound()

        review_data_dict = review_data.model_dump()

        new_review = Reviews(**review_data_dict)
        new_review.book = book
        new_review.user = user

        session.add(new_review)
        await session.commit()
        await session.refresh(new_review)
        return new_review
    
    async def update_review(
        self,
        review_uid: str,
        review_data: ReviewUpdateSchema,
        session: AsyncSession
    ) -> Reviews:
        statement = select(Reviews).where(Reviews.uid == review_uid)
        result = await session.exec(statement)
        review = result.first()
        if review:
            review_data_dict = review_data.model_dump(exclude_unset=True)
            for key, value in review_data_dict.items():
                setattr(review, key, value)
            review.updated_at = datetime.now(tz=timezone.utc)
            session.add(review)
            await session.commit()
            return review

        raise ReviewNotFound()
    
    async def delete_review(self, review_uid:str, session: AsyncSession) -> Reviews:
        review = await self.get_a_review(review_uid=review_uid, session=session)
        await session.delete(review)
        await session.commit()
        return