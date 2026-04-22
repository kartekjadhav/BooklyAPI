import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from src.dependencies.get_current_user import get_current_user
from src.schemas.review_schemas import ReviewCreateSchema, ReviewSchema
from src.db.db import get_session
from src.services.review_service import ReviewServices
from src.models.all_models import Users


review_router = APIRouter()
review_services = ReviewServices()

@review_router.post("/book/{book_uid}", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED)
async def add_book_review(
    book_uid: str,
    review_data: ReviewCreateSchema,
    current_user:Users=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    try:
        review = await review_services.add_book_review(
            user_email=current_user.email,
            book_uid=book_uid,
            review_data=review_data,
            session=session
        )
        return review
    except HTTPException:
        raise
    except Exception as e:
        logging.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
