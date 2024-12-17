import os

from celery import Celery
from django.conf import settings
from telegrambot.container import WorkerContainer
from celery.signals import worker_process_init
# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sauna_landing.settings")

sauna_landing = Celery("sauna_landing")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
sauna_landing.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
sauna_landing.autodiscover_tasks()

@worker_process_init.connect
def init_di_container(sender, **kwargs) -> None:
    container = WorkerContainer()
    container.config.telegrambot_key.from_value(settings.TELEGRAMBOT_KEY)
    container.wire(modules=["telegrambot.tasks", ])