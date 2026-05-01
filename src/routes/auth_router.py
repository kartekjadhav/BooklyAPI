from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from src.services.user_service import UserService
from src.schemas.UserSchemas import  UserCreateSchema, UserLoginSchema, UsersSchemaWithBooks, NewUsersCreatedSchema, PasswordResetConfirmSchema, PasswordResetRequestSchema
from src.schemas.token import TokenPayLoad
from src.db.db import get_session
from src.utils.passwdUtil import verify_password
from src.utils.jwtUtil import generate_access_token
from datetime import timedelta, datetime
from src.dependencies.bearer import RefreshTokenBearer, AccessTokenBearer
from src.redis.redis import add_jti_to_blocklist
from src.dependencies.get_current_user import get_current_user
from src.dependencies.role_checker import RoleChecker
from src.errors.errors import UserAlreadyExists, InvalidCredentials, InvalidOrExpiredToken, UserNotFound
from src.mail import create_message, EmailAddressesSchema, fastmail
from src.email_templates.test_template import generate_template
from src.email_templates import generate_email_verification_template, generate_reset_password_template
from src.utils.token_util import generate_serializer_token, verify_serializer_token, email_verify_serializer, password_reset_serializer
from src.schemas.setting import setting
from src.utils.passwdUtil import generate_password_hash
from src.celery_app import send_email_task


auth_router = APIRouter()
user_service = UserService()
refresh_token_bearer = RefreshTokenBearer()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(allowed_roles=["user"])

REFRESH_TOKEN_EXPIRY = 2 # In days


@auth_router.post("/signup", response_model=NewUsersCreatedSchema, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateSchema, session: AsyncSession = Depends(get_session)):
    user_email = user_data.email
    user_exists = await user_service.user_exits(email=user_email, session=session)

    if user_exists:
        raise UserAlreadyExists()
    
    new_user = await user_service.create_user(user_data=user_data, session=session)

    if new_user:

        email_verification_token = generate_serializer_token(data={'email': user_email}, serializer=email_verify_serializer)

        link = f"http://{setting.DOMAIN}/api/v1/auth/verify_email/{email_verification_token}"

        send_email_task.delay(
            recipients=[user_email],
            subject="Verify your Email!",
            body=generate_email_verification_template(username=f"{new_user.first_name} {new_user.last_name}", verification_link=link)
        )

        return JSONResponse(
            content={
                "message": "Signed up successfully. Please verify your email on the link sent to you.",
                "user": new_user.model_dump(mode="json")
            },
            status_code=status.HTTP_200_OK
        )

    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@auth_router.get("/verify_email/{token}")
async def verify_email_token(token:str, session:AsyncSession=Depends(get_session)):
    token_data = verify_serializer_token(token=token, serializer=email_verify_serializer)
    user_email = token_data.get('email')
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()
        await user_service.update_user(user=user, user_data={'verified': True}, session=session)
        return JSONResponse(
            content={
                "message": "Email verified successfully!"
            },
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
            content={
                "message": "Error occured during email verification"
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


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

    raise InvalidCredentials()

@auth_router.get("/me", response_model=UsersSchemaWithBooks, status_code=status.HTTP_200_OK)
async def get_current_user_details(
    user = Depends(get_current_user),
    _: bool = Depends(role_checker)
):
    return user

@auth_router.get("/refresh")
async def get_access_token(tokenData: TokenPayLoad = Depends(refresh_token_bearer)):
    expiry_timestamp = tokenData["exp"]
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = generate_access_token(user_data=tokenData["user"])
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
    
    raise InvalidOrExpiredToken()


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


@auth_router.post("/send_email")
async def send_email(recipients:EmailAddressesSchema, subject:str, body:str=None):
    body = generate_template(username="Kartek", message="Hope you are doing well, this is a test email and dont reply.")

    send_email_task.delay(
        recipients=recipients.model_dump().get('emails'),
        subject=subject,
        body=body
    )

    return JSONResponse(
        content="Email sent successfully",
        status_code=status.HTTP_200_OK
    )


@auth_router.post("/reset_password")
async def reset_password_initiate(user_data:PasswordResetRequestSchema, session:AsyncSession=Depends(get_session)):
    user_email = user_data.email

    email_verification_token = generate_serializer_token(data={'email': user_email}, serializer=password_reset_serializer)

    link = f"http://{setting.DOMAIN}/api/v1/auth/reset_password_confirm/{email_verification_token}"

    send_email_task(
        recipients=[user_email],
        subject="Verify your Email!",
        body=generate_reset_password_template(reset_link=link)
    )

    return JSONResponse(
        content={
            "message": "Please follow the instruction sent to your email",
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.post("/reset_password_confirm/{token}")
async def reset_password_initiate(token: str, reset_password_data: PasswordResetConfirmSchema, session:AsyncSession=Depends(get_session)):
    if reset_password_data.new_password != reset_password_data.confirm_password:
        return JSONResponse(
            content={
                "message": "New password and confirm password should be same"
            },
            status_code=status.HTTP_400_BAD_REQUEST
        )
    
    token_data = verify_serializer_token(token=token, serializer=password_reset_serializer)
    user_email = token_data.get('email')
    if user_email:
        user = await user_service.get_user_by_email(user_email, session)
        if not user:
            raise UserNotFound()
        
        new_password_hash = generate_password_hash(password=reset_password_data.new_password)
        await user_service.update_user(user=user, user_data={'password_hash': new_password_hash}, session=session)
        return JSONResponse(
            content={
                "message": "Password Resetted successfully!"
            },
            status_code=status.HTTP_200_OK
        )
    return JSONResponse(
        content={
            "message": "Error occured during verificationpassword reset"
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )