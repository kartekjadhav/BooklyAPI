from fastapi.requests import Request
from fastapi.responses import JSONResponse
from typing import Callable, Any

class BooklyException(Exception):
    """Base exception clss for all the exceptions in Bookly application"""
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