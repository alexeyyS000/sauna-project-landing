from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(null=False, unique=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    is_active_tg_alerting = models.BooleanField(null=False, default=False)
    updated = models.DateTimeField(auto_now=True)


class CallbackRequest(models.Model):


    class State(models.TextChoices):
        NEW = 'new', 'New'
        IN_PROCESS = 'in_process', 'In Process'
        COMPLETED = 'completed', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата обращения")
    state = models.CharField(
        max_length=20,
        choices=State.choices,
        default=State.NEW,
        verbose_name="Состояние заявки"
    )
    attempts = models.IntegerField(default=0, null=False)