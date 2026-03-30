from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.utils.jwtUtil import verify_access_token
from typing import List
from src.schemas.token import TokenPayLoad

class AccessTokenBearer(HTTPBearer):
    def __init__(self, auto_error = True) -> TokenPayLoad:
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        creds =  await super().__call__(request)

        is_token_valid, user_data = self.token_valid(token=creds.credentials)

        if not is_token_valid:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Access Token"
            )
        
        if user_data and user_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide Access Token"
            )
        
        return user_data
    
    def token_valid(self, token: str) -> tuple[bool, dict | None]:
        user_data = verify_access_token(access_token=token)
        return (True, user_data) if user_data is not None else (False, None)