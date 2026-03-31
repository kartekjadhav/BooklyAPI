from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from .bearer import AccessTokenBearer
from src.schemas.token import TokenPayLoad
from src.db.db import get_session
from src.services.UserService import UserService
from src.models.UserModel import Users

async def get_current_user(
    tokenData: TokenPayLoad = Depends(AccessTokenBearer()),
    session: AsyncSession = Depends(get_session)
) -> Users | None:
    user_email = tokenData['user']['email']
    user = await UserService().get_user_by_email(email=user_email, session=session)
    return user