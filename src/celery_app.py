from typing import List
from celery import Celery
from src.schemas.setting import setting
from src.mail import create_message, fastmail
from asgiref.sync import async_to_sync

celery_broker_url = f"{setting.REDIS_URL}/1"
celery_result_backend_url = f"{setting.REDIS_URL}/1"

celery_app = Celery(
    "tasks",
    backend=celery_result_backend_url,
    broker=celery_broker_url
)

@celery_app.task
def send_email_task(recipients:List[str], subject:str, body:str):
    msg = create_message(
        recipients=recipients,
        subject=subject,
        body=body
    )

    async_to_sync(fastmail.send_message)(message=msg)
    print(f"Email sent to {recipients} with subject {subject}")

# celery -A src.celery_app:celery_app worker --pool=solo --loglevel=info

# celery -A src.celery_app:celery_app flower --port=5555