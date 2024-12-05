import django

from telegrambot.container import BotContainer

django.setup()
from telegrambot.bot import handlers
import structlog
from django.conf import settings
logger = structlog.get_logger("telegram_bot")

from telegram.ext import CommandHandler, CallbackQueryHandler


def main() -> None:
    """Run the bot."""


    updater = container.updater()

    # updater = Updater(token=settings.TELEGRAMBOT_KEY, use_context=True)

    updater.dispatcher.add_handler(CommandHandler("start", handlers.start_command))
    #
    updater.dispatcher.add_handler(CommandHandler("unsubscribe", handlers.unsubscribe_command))
    #
    updater.dispatcher.add_handler(CommandHandler("subscribe", handlers.subscribe_command))

    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.handle_button_click, pattern='rrrrrr'))
    updater.dispatcher.add_handler(CommandHandler("start2", handlers.start2))

    updater.dispatcher.add_handler(CallbackQueryHandler(handlers.button, pattern='button'))

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    container = BotContainer()
    container.config.telegrambot_key.from_value(settings.TELEGRAMBOT_KEY)
    container.wire(modules=[__name__, ])
    main()