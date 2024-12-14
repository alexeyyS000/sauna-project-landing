from django.contrib import admin
from .models import User, CallbackRequest


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "phone_number",
        "telegram_id",
        "is_active_tg_alerting",
        "updated",
    )
    search_fields = ("username", "phone_number", "telegram_id")
    list_filter = ("is_active_tg_alerting",)


@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "state", "created_at")
    list_filter = ("state", "created_at")
    search_fields = ("user__username",)
