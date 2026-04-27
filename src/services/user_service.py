from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.models import Users
from src.schemas.UserSchemas import UserCreateSchema, UsersSchema
from src.utils.passwdUtil import generate_password_hash, verify_password

class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> Users | None:
        try:
            statement = select(Users).where(Users.email == email)
            result = await session.exec(statement)
            user = result.first()
            return user if user else None
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def user_exits(self, email: str, session: AsyncSession) -> bool:
        try:
            user = await self.get_user_by_email(email=email, session=session)
            return True if user is not None else False
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    async def create_user(self, user_data: UserCreateSchema, session: AsyncSession) -> Users:
        try:
            user_data_dict = user_data.model_dump()
            new_user = Users(**user_data_dict)
            new_user.password_hash = generate_password_hash(user_data_dict['password'])
            new_user.role = "user"
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    async def update_user(self, user:Users, user_data:dict, session:AsyncSession) -> Users:
        try:
            for key, value in user_data.items():
                setattr(user, key, value)
            user.updated_at = datetime.now(tz=timezone.utc)
            session.add(user)
            await session.commit()
            return user
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)