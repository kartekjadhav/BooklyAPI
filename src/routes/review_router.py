from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import Response
from sqlmodel.ext.asyncio.session import AsyncSession
from src.dependencies.get_current_user import get_current_user
from src.schemas.review_schemas import ReviewCreateSchema, ReviewSchema, ReviewUpdateSchema
from src.schemas.token import TokenPayLoad
from src.dependencies.bearer import AccessTokenBearer
from src.db.db import get_session
from src.services.review_service import ReviewServices
from src.models.all_models import Users
from src.dependencies.role_checker import RoleChecker



review_router = APIRouter()
review_services = ReviewServices()
access_token_bearer = AccessTokenBearer()
role_checker = Depends(RoleChecker(allowed_roles=['user', 'admin']))

# Get all Reviews
@review_router.get("/", response_model=List[ReviewSchema], status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_all_reviews(tokenData: TokenPayLoad = Depends(access_token_bearer), session: AsyncSession = Depends(get_session)):
    all_reviews = await review_services.get_all_reviews(session=session)
    return all_reviews

# Get a review
@review_router.get("/{review_uid}", response_model=ReviewSchema, status_code=status.HTTP_200_OK, dependencies=[role_checker])
async def get_a_review(review_uid:str, tokenData: TokenPayLoad = Depends(access_token_bearer), session: AsyncSession = Depends(get_session)):
    review = await review_services.get_a_review(review_uid=review_uid, session=session)
    return review

# Create a Review
@review_router.post("/book/{book_uid}", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def add_book_review(
    book_uid: str,
    review_data: ReviewCreateSchema,
    current_user:Users=Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    review = await review_services.add_book_review(
        user_email=current_user.email,
        book_uid=book_uid,
        review_data=review_data,
        session=session
    )
    return review


# Update a Review
@review_router.patch("/{review_uid}", response_model=ReviewSchema, status_code=status.HTTP_201_CREATED, dependencies=[role_checker])
async def update_review(
    review_uid: str,
    review_data: ReviewUpdateSchema, 
    tokenData: TokenPayLoad = Depends(access_token_bearer), 
    session: AsyncSession = Depends(get_session)
):
    updated_review = await review_services.update_review(review_uid=review_uid, review_data=review_data, session=session)
    return updated_review

# Delete a Review
@review_router.delete("/{review_uid}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[role_checker])
async def delete_review(review_uid:str, tokenData: TokenPayLoad = Depends(access_token_bearer), session: AsyncSession = Depends(get_session)):
    await review_services.delete_review(review_uid=review_uid, session=session)
    return Response(status_code=status.HTTP_204_NO_CONTENT)