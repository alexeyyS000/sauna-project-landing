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
    telegram_id = models.BigIntegerField(
        null=True, blank=True
    )
    is_active_tg_alerting = models.BooleanField(null=False, default=False)
    updated = models.DateTimeField(auto_now=True)


class CallbackRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name="заявка активна?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата обращения")
