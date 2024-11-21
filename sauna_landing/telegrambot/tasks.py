import json


from celery import shared_task
from django.contrib.auth import get_user_model


@shared_task(bind=True, max_retries=3)
def send_message_callback(
    self,
    test
) -> int:


    return 0

