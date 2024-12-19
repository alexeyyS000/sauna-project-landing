import django

from telegrambot.container import BotContainer

django.setup()
from telegram.ext import TypeHandler
from telegram import Update
from telegrambot.bot import handlers
import structlog
from django.conf import settings
logger = structlog.get_logger("telegram_bot")

from telegram.ext import CommandHandler, CallbackQueryHandler


def main() -> None:
    """Run the bot."""


    updater = container.updater()

    updater.dispatcher.add_handler(TypeHandler(Update, handlers.get_user), -1)

    updater.dispatcher.add_handler(CommandHandler("start", handlers.start_command))

    updater.dispatcher.add_handler(CommandHandler("unsubscribe", handlers.unsubscribe_command))


    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.show_phone_handler, pattern=r"^show_phone_"))

    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.process_request_handler, pattern='^processed_'))


    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    container = BotContainer()
    container.config.telegrambot_key.from_value(settings.TELEGRAMBOT_KEY)
    container.wire(modules=[__name__, ])
    main()