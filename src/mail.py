from typing import List
from pydantic import BaseModel, EmailStr
from pathlib import Path
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from src.schemas.setting import setting


BASE_PATH = Path(__file__).parent

class EmailAddressesSchema(BaseModel):
    emails: List[EmailStr]


conf = ConnectionConfig(
    MAIL_USERNAME = setting.MAIL_USERNAME,
    MAIL_PASSWORD = setting.MAIL_PASSWORD,
    MAIL_FROM = setting.MAIL_FROM,
    MAIL_PORT = setting.MAIL_PORT,
    MAIL_SERVER = setting.MAIL_SERVER,
    MAIL_FROM_NAME = setting.MAIL_FROM_NAME,
    MAIL_STARTTLS = setting.MAIL_STARTTLS,
    MAIL_SSL_TLS = setting.MAIL_SSL_TLS,
    USE_CREDENTIALS = setting.USE_CREDENTIALS,
    VALIDATE_CERTS = setting.VALIDATE_CERTS,
    TEMPLATE_FOLDER = Path(BASE_PATH, 'email_templates')
)


fastmail = FastMail(conf)

def create_message(recipients:list, subject:str, body:str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype=MessageType.html
    )

    return message