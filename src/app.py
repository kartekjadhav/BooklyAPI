from fastapi import FastAPI, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from src.routes import book_router, auth_router, review_router
from contextlib import asynccontextmanager
from src.db.db import init_db
from src.redis.redis import token_blocklist
from src.errors.errors import (
    BookAlreadyExists, 
    BookNotFound, 
    UserAlreadyExists, 
    UserNotFound, 
    InsufficientPrivileges, 
    InvalidCredentials, 
    InvalidOrExpiredToken, 
    InvalidOrRevokedToken,
    ReviewNotFound,
    create_exception_handler
)


REDIS_CONNECTION_RETRIES = 6


@asynccontextmanager
async def life_span(app:FastAPI):
    print("Server is starting 🟢")

    # Check Postgres DB connectivity
    await init_db()

    # Check redis connectivity
    for try_attempt in range(REDIS_CONNECTION_RETRIES):
        try:
            redis_connection = await token_blocklist.ping()
            if redis_connection:
                print("✅ Redis connection working fine")
                break
        except Exception as e:
            if try_attempt == REDIS_CONNECTION_RETRIES - 1:
                print("❌ Redis connection failed")
                raise Exception("❌ Redis connection not working")  # crash app
            else:
                print(f"Couldn't establish Redis connection, retrying again (attempt - {try_attempt+1} / {REDIS_CONNECTION_RETRIES-1})")
    yield
    print("Server is stopping 🔴")

app = FastAPI(lifespan=life_span, title="Bookly", description="A REST API for book review web service", version="v1")

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Invalid email or password",
            "error_code": "invalid_credentials"
        }
    )
)

app.add_exception_handler(
    BookAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "message": "Book already exists",
            "error_code": "book_already_exists"
        }
    )
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": "Book not found",
            "error_code": "book_not_found"
        }
    )
)

app.add_exception_handler(
    UserAlreadyExists,
    create_exception_handler(
        status_code=status.HTTP_409_CONFLICT,
        detail={
            "message": "User with this email already exists",
            "error_code": "user_already_exists"
        }
    )
)

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": "User not found",
            "error_code": "user_not_found"
        }
    )
)

app.add_exception_handler(
    InsufficientPrivileges,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        detail={
            "message": "Insufficient Privileges",
            "error_code": "insufficient_privileges"
        }
    )
)

app.add_exception_handler(
    InvalidOrExpiredToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Invalid or expired token",
            "error_code": "invalid_token"
        }
    )
)

app.add_exception_handler(
    InvalidOrRevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "message": "Invalid or revoked token",
            "error_code": "invalid_or_revoked_token"
        }
    )
)

app.add_exception_handler(
    ReviewNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "message": "Review not found",
            "error_code": "review_not_found"
        }
    )
)

@app.exception_handler(500)
async def internal_server_error(request: Request, exc):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": f"Oops! Something went wrong.", "error_code": "internal_server_error"}
    )   


# User auth Router
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])

# Book Router
app.include_router(book_router, prefix="/api/v1/books", tags=["books"])

# Review Router
app.include_router(review_router, prefix="/api/v1/reviews", tags=["review"])