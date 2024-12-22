from django.contrib.auth import get_user_model
from telegrambot.utils.template import render_template
UserModel = get_user_model()
from django.shortcuts import get_object_or_404
from users.models import CallbackRequest
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
import structlog
logger = structlog.get_logger("telegram_bot")
from django.template.loader import render_to_string

def start_command(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    user = update.effective_user
    telegram_id = user.id

    logger.info("Received /start command", user_tg_id=telegram_id)

    user = context.chat_data['user']
    if user.is_active_tg_alerting is False:
        user.is_active_tg_alerting = True
        user.save()
    message_html = render_to_string('start_message.html', )
    update.message.reply_text(
        message_html,
        parse_mode='HTML'
    )

def unsubscribe_command(update: Update, context: CallbackContext) -> None:
    """Handle the /unsubscribe command."""
    tg_user = update.effective_user
    telegram_id = tg_user.id

    logger.info("Received /unsubscribe command", user_tg_id=telegram_id)

    user = context.chat_data['user']
    if user:
        user.is_active_tg_alerting = False
        user.save()
        message_html = render_to_string('unsubscribe_message.html', )
        update.message.reply_text(
            message_html,
            parse_mode='HTML'
        )
    else:
        update.message.reply_text("Вас еще нет в базе.")


def process_request_handler(update: Update, context: CallbackContext):
    logger.info("Received /process_request_handler callback")

    query = update.callback_query
    query.answer()

    callback_request_id = int(query.data.split('_')[1])
    callback_request = get_object_or_404(CallbackRequest, id=callback_request_id)

    if callback_request.state != CallbackRequest.State.COMPLETED:
        callback_request.state = CallbackRequest.State.COMPLETED
        callback_request.save()

        query.edit_message_text(text="Заявка успешно обработана.", reply_markup=None)
    else:
        query.edit_message_text(text="Заявка уже была завершена.", reply_markup=None)



def show_phone_handler(update: Update, context: CallbackContext):
    logger.info("Received /show_phone_handler callback")
    query = update.callback_query
    query.answer()

    callback_data = query.data

    callback_request_id = int(callback_data.split('_')[2])
    callback_request = get_object_or_404(CallbackRequest, id=callback_request_id)

    # Проверка состояния заявки
    if callback_request.state == CallbackRequest.State.NEW:
        callback_request.state = CallbackRequest.State.IN_PROCESS
        callback_request.save()

        new_keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("✅ Завершить обработку", callback_data=f"processed_{callback_request_id}")],
            ]
        )

        message = f"Номер телефона пользователя: {callback_request.user.phone_number}"
        query.edit_message_text(text=message, reply_markup=new_keyboard)
    else:
        query.edit_message_text(text="Эта заявка уже в обработке или обработана.")


def get_user(
    update: Update,
    context: CallbackContext,
) -> None:
    """
    Get or create user.
    """
    current_user = update.effective_user
    chat_data = context.chat_data

    user = UserModel.objects.filter(telegram_id=current_user.id).first()#get_or_create
    if user:
        chat_data["user"] = user
    else:
        update.message.reply_text("Вас еще нет в базе.")