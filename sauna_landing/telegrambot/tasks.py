import json

from telegram.ext import Updater
from celery import shared_task
from django.contrib.auth import get_user_model
from telegrambot.bot.__main__ import bot_instance
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

UserModel = get_user_model()


@shared_task(
    name="send_notification",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def send_notification(
    admin_tg_id: int,
    callback_request_id: int,
    user_phone_number: str,
    user_first_name: str,
):

    message = f"Пользователь {user_first_name} с номером {user_phone_number} запросил обратный звонок."
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "✅ Обработано", callback_data=f"process_{callback_request_id}"
                )
            ]
        ]
    )
    updater = Updater(
        token="7511137111:AAEh8u8xihiybbD3ARyGat8m1aMl-qvqy_M", use_context=True
    )
    updater.bot.send_message(chat_id=admin_tg_id, text=message, reply_markup=keyboard)
    # bot_instance.send_message(chat_id=admin_tg_id, text=message, reply_markup=keyboard)


@shared_task(
    name="send_notifications",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def send_notifications(callback_request_id, user_phone_number, user_first_name) -> None:
    admins = UserModel.objects.filter(
        telegram_id__isnull=False, is_active_tg_alerting=True
    )
    for admin in admins:
        send_notification.delay(
            admin_tg_id=admin.telegram_id,
            callback_request_id=callback_request_id,
            user_phone_number=user_phone_number,
            user_first_name=user_first_name,
        )
