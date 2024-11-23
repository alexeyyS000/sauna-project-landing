from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext

from django.contrib.auth import get_user_model

UserModel = get_user_model()

SAVE = 1





def start(update: Update, context: CallbackContext) -> int:
    user = update.effective_user
    telegram_id = user.id

    print('STARTTT')
    if UserModel.objects.filter(telegram_id=telegram_id).exists():
        update.message.reply_text("Вы уже зарегистрированы!")
        return ConversationHandler.END


    update.message.reply_text("Пожалуйста, введите ваше имя:")
    print('Asking for name. Switching to SAVE state.')
    return SAVE


def enter_name(update: Update, context: CallbackContext) -> int:
    print('enter_name')
    user = update.effective_user
    name = update.message.text.strip()


    UserModel.objects.create(
        telegram_id=user.id,
        name=name,
        username=user.username,
    )

    update.message.reply_text(f"Спасибо, {name}! Вы зарегистрированы.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    print('cancel')
    update.message.reply_text("Регистрация отменена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END



start_conv = ConversationHandler(
    persistent=True,
    name="start",
    entry_points=[CommandHandler("start", start)],
    states={
        SAVE: [MessageHandler(Filters.text, enter_name)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)


