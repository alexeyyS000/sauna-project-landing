from django.contrib.auth import get_user_model

UserModel = get_user_model()


from telegram import Update
from telegram.ext import CallbackContext
import structlog

logger = structlog.get_logger("telegram_bot")


def start_command(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    user = update.effective_user
    telegram_id = user.id

    logger.info("Received /start command", user_tg_id=telegram_id)

    user = UserModel.objects.filter(telegram_id=telegram_id).first()
    if user:
        user.is_active_tg_alerting = True
        user.save()
        update.message.reply_text(
            "Теперь вы получаете уведомления об обратных звонках. Нажмите /unsubscribe чтобы перестать получать сообщения"
        )
    else:
        update.message.reply_text("Вас еще нет в базе.")


def unsubscribe_command(update: Update, context: CallbackContext) -> None:
    """Handle the /unsubscribe command."""
    tg_user = update.effective_user
    telegram_id = tg_user.id

    logger.info("Received /unsubscribe command", user_tg_id=telegram_id)

    user = UserModel.objects.filter(telegram_id=telegram_id).first()
    if user:
        user.is_active_tg_alerting = False
        user.save()
        update.message.reply_text(
            "Теперь вы не получаете уведомления об обратных звонках. Нажмите /subscribe чтобы начать получать сообщения"
        )
    else:
        update.message.reply_text("Вас еще нет в базе.")


def subscribe_command(update: Update, context: CallbackContext) -> None:
    """Handle the /subscribe command."""
    tg_user = update.effective_user
    telegram_id = tg_user.id

    logger.info("Received /subscribe command", user_tg_id=telegram_id)

    user = UserModel.objects.filter(telegram_id=telegram_id).first()
    if user:
        user.is_active_tg_alerting = True
        user.save()
        update.message.reply_text(
            "Теперь вы получаете уведомления об обратных звонках. Нажмите /unsubscribe чтобы перестать получать сообщения"
        )
    else:
        update.message.reply_text("Вас еще нет в базе.")
