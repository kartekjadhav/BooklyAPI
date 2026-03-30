from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.services.UserService import UserService
from src.schemas.UserSchemas import  UserCreateSchema, UsersSchema, UserLoginSchema
from src.schemas.token import TokenPayLoad
from src.db.db import get_session
from src.utils.passwdUtil import verify_password
from src.utils.jwtUtil import generate_access_token
from datetime import timedelta, datetime
from src.dependencies.bearer import RefreshTokenBearer, AccessTokenBearer
from src.redis.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()

REFRESH_TOKEN_EXPIRY = 2 # In days


@auth_router.post("/signup", response_model=UsersSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user_email = user_data.email
    user_exists = await user_service.user_exits(email=user_email, session=session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User with given email already exists")
    
    new_user = await user_service.create_user(user_data=user_data, session=session)

    return new_user

@auth_router.post("/login", status_code=status.HTTP_200_OK)
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

@auth_router.get("/refresh_token")
async def get_access_token(tokenData: TokenPayLoad = Depends(refresh_token_bearer)):
    expiry_timestamp = tokenData["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = generate_access_token(user_data=tokenData["user"])
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
    
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid or expired token")


@auth_router.get("/logout")
async def logout(tokenData: TokenPayLoad = Depends(access_token_bearer)):
    jti = tokenData["jti"]
    await add_jti_to_blocklist(
        jti=jti
    )
    return JSONResponse(
        content={
            "message": "Logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )