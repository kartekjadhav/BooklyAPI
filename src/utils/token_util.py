import logging
from itsdangerous.url_safe import URLSafeTimedSerializer
from src.schemas.setting import setting

email_token_serializer = URLSafeTimedSerializer(secret_key=setting.ITSDANGEROUS_SECRET_KEY, salt="email-verification")

def generate_email_verification_token(data:dict) -> str:
    token = email_token_serializer.dumps(data)
    return token

def verify_email_verification_token(token:str) -> dict:
    try:
        token_data = email_token_serializer.loads(token, max_age=10800)
        return token_data
    except Exception as e:
        logging.error(e)
        return None