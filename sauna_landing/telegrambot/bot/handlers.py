from django.contrib.auth import get_user_model

UserModel = get_user_model()

from users.models import CallbackRequest
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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


def handle_button_click(update, context):
    query = update.callback_query
    query.answer()

    callback_data = query.data
    if callback_data.startswith("process_"):#patametr in calbachHandler
        request_id = int(callback_data.split("_")[1])#TODO число в регулярке после нижнего подчеркивания
        try:

            callback_request = CallbackRequest.objects.get(id=request_id)#TODO 3 состояния новая в обработке и завершенная  , номер телефона скарыт и показывается только при переходе заявки в статус обработки при этом номер становится недоступен для другиз одминов
            if callback_request.is_active:
                callback_request.is_active = False
                callback_request.save()

                query.edit_message_text(
                    text=f"Заявка обработана.\nПользователь {callback_request.user.first_name} с номером {callback_request.user.phone_number} запросил обратный звонок."#TODO to template
                )
        except CallbackRequest.DoesNotExist:
            query.edit_message_text(text="Заявка не найдена или уже обработана.")



def start2(update: Update, context: CallbackContext) -> None:
    logger.info("Received /start2 command",)
    keyboard = [
        [InlineKeyboardButton("Кнопка 1", callback_data="button")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Выберите кнопку:", reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    logger.info("Received /button command", )
    query = update.callback_query
    query.answer()


    query.edit_message_text(text="Вы нажали кнопку 1!")

