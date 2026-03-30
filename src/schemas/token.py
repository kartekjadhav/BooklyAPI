from typing import TypedDict


class UserPayload(TypedDict):
    uid: str
    email: str

class TokenPayLoad(TypedDict):
    user: UserPayload
    jti: str
    exp: int
    refresh: bool