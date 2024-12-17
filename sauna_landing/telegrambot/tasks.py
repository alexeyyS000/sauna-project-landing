from telegram.ext import Updater
from celery import shared_task
from django.contrib.auth import get_user_model
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from dependency_injector.wiring import inject, Provide
from telegrambot.container import WorkerContainer
UserModel = get_user_model()


@shared_task(
    name="send_notification",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
@inject
def send_notification(
    admin_tg_id: int,
    callback_request_id: int,
    user_first_name: str,
    bot: Updater = Provide[WorkerContainer.bot],
):

    message = f"Пользователь {user_first_name} запросил обратный звонок."
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "📞 Показать номер телефона", callback_data=f"show_phone_{callback_request_id}"#регулярка
                )
            ],

        ]
    )
    bot.send_message(chat_id=admin_tg_id, text=message, reply_markup=keyboard)



@shared_task(
    name="send_notifications",
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 5},
)
def send_notifications(callback_request_id, user_first_name) -> None:
    admins = UserModel.objects.filter(
        telegram_id__isnull=False, is_active_tg_alerting=True
    )
    for admin in admins:
        send_notification.delay(
            admin_tg_id=admin.telegram_id,
            callback_request_id=callback_request_id,
            user_first_name=user_first_name,
        )
