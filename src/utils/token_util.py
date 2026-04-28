import logging
from itsdangerous.url_safe import URLSafeTimedSerializer
from src.schemas.setting import setting

def create_serializer(salt: str) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(
        secret_key=setting.ITSDANGEROUS_SECRET_KEY,
        salt=salt
    )

email_verify_serializer = create_serializer(salt="email-verification")
password_reset_serializer = create_serializer(salt="password-reset")

def generate_serializer_token(data:dict, serializer: URLSafeTimedSerializer) -> str:
    token = serializer.dumps(data)
    return token

def verify_serializer_token(token:str, serializer: URLSafeTimedSerializer) -> dict:
    try:
        token_data = serializer.loads(token, max_age=10800)
        return token_data
    except Exception as e:
        logging.error(e)
        return None