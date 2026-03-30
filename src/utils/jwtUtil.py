import jwt
import uuid
from datetime import timedelta, datetime, timezone
from src.schemas.setting import setting
import logging

ACCESS_TOKEN_EXPIRY = 3600 # In seconds

def generate_access_token(user_data: dict, refresh: bool = False, expiry: timedelta = None):
    payload = {}
    payload['user'] = user_data
    payload['jti'] = str(uuid.uuid4())
    payload['exp'] = datetime.now(timezone.utc) + timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    payload['refresh'] = refresh

    access_token = jwt.encode(
        payload=payload,
        key=setting.JWT_SECRET,
        algorithm=setting.JWT_ALGORITHM
    )

    return access_token

def verify_access_token(access_token: str):
    try:
        decode_data = jwt.decode(
            jwt=access_token,
            key=setting.JWT_SECRET,
            algorithms=[setting.JWT_ALGORITHM]
        )
        return decode_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None