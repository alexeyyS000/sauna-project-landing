from django.conf import settings
from telegram.ext import Updater
from celery import shared_task
from django.contrib.auth import get_user_model
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dependency_injector.wiring import inject, Provide
from telegrambot.container import BotContainer
UserModel = get_user_model()

container = BotContainer()
container.config.telegrambot_key.from_value(settings.TELEGRAMBOT_KEY)
container.wire(modules=[__name__, ])

@shared_task(
    name="send_notification",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
@inject
def send_notification(
    admin_tg_id: int,
    callback_request_id: int,
    user_phone_number: str,
    user_first_name: str,
    updater: Updater = Provide[BotContainer.updater],
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
    updater = Updater(token = settings.TELEGRAMBOT_KEY)
    updater.bot.send_message(chat_id=admin_tg_id, text=message, reply_markup=keyboard)



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
