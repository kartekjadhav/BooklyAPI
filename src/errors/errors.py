from fastapi import FastAPI, status
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from typing import Callable, Any

class BooklyException(Exception):
    """Base exception clss for all the exceptions in Bookly application"""
    pass

class AccountNotVerified(BooklyException):
    """Account not verified exception"""
    pass

class UserAlreadyExists(BooklyException):
    """User already exists exception"""
    pass

class UserNotFound(BooklyException):
    """User not found exception"""
    pass

class InvalidCredentials(BooklyException):
    """Invalid credentials exception"""
    pass

class InvalidOrExpiredToken(BooklyException):
    """Invalid or Expired token exception"""
    pass

class InvalidOrRevokedToken(BooklyException):
    """Revoked token exception"""
    pass

class InsufficientPrivileges(BooklyException):
    """Insufficient privileges exception"""
    pass

class BookNotFound(BooklyException):
    """Book not found exception"""
    pass

class BookAlreadyExists(BooklyException):
    """Book already exists exception"""
    pass

class ReviewNotFound(BooklyException):
    """Book not found exception"""
    pass

def create_exception_handler(status_code: int, detail: Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request: Request, exc):
        return JSONResponse(
            content=detail,
            status_code=status_code
        )
    
    return exception_handler

def register_all_errors(app: FastAPI):
    app.add_exception_handler(
        AccountNotVerified,
        create_exception_handler(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "message": "Your email has not been verified yet",
                "error_code": "account_not_verified",
                "resoultion": "Please verify your email to proceed"
            }
        )
    )

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