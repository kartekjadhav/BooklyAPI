from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.services.UserService import UserService
from src.schemas.UserSchemas import  UserCreateSchema, UsersSchema, UserLoginSchema
from src.db.db import get_session
from src.utils.passwdUtil import verify_password
from src.utils.jwtUtil import generate_access_token
from datetime import timedelta  

user_router = APIRouter()
user_service = UserService()

REFRESH_TOKEN_EXPIRY = 2 # In days


@user_router.post("/signup", response_model=UsersSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user_email = user_data.email
    user_exists = await user_service.user_exits(email=user_email, session=session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with given email already exists")
    
    new_user = await user_service.create_user(user_data=user_data, session=session)

    return new_user

@user_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(user_login_data: UserLoginSchema, session: AsyncSession = Depends(get_session)):
    user_email = user_login_data.email
    user = await user_service.get_user_by_email(email=user_email, session=session)
    if user is not None:
        is_password_valid = verify_password(original_password=user_login_data.password, hashed_password=user.password_hash)
        if is_password_valid:
            access_token = generate_access_token(
                user_data={
                    "uid": str(user.uid),
                    "email": user.email
                }
            )

            refresh_token = generate_access_token(
                user_data={
                    "uid": str(user.uid),
                    "email": user.email
                },
                refresh = True,
                expiry = timedelta(days=REFRESH_TOKEN_EXPIRY)
            )

            return JSONResponse(
                content={
                    "message": "Login Successfull",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {
                        "uid": str(user.uid),
                        "email": user.email
                    }
                }
            )

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")