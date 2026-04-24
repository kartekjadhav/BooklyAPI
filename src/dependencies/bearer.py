from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from src.utils.jwtUtil import verify_access_token
from src.schemas.token import TokenPayLoad
from src.redis.redis import token_in_blocklist
from src.errors.errors import InvalidOrExpiredToken, InvalidOrRevokedToken

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True) -> None:
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> TokenPayLoad:
        creds =  await super().__call__(request)

        is_token_valid, tokenData = self.token_valid(token=creds.credentials)

        if not is_token_valid:
            raise InvalidOrExpiredToken()
        
        if not tokenData['jti'] or await token_in_blocklist(tokenData['jti']):
            raise InvalidOrRevokedToken()
        
        self.verify_token_data(tokenData)
        
        return tokenData
    
    def token_valid(self, token: str) -> tuple[bool, dict | None]:
        token_data = verify_access_token(access_token=token)
        return (True, token_data) if token_data is not None else (False, None)
    
    def verify_token_data(self, tokenData: TokenPayLoad):
        raise NotImplementedError("Subclass must implement this method")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, tokenData: TokenPayLoad):        
        if not tokenData or tokenData['refresh']:
            raise InvalidOrRevokedToken()

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, tokenData: TokenPayLoad):        
        if not tokenData or 'refresh' not in tokenData or not tokenData['refresh']:
            raise InvalidOrRevokedToken()