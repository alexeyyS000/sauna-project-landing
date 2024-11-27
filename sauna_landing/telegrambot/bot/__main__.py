import django

django.setup()
from telegrambot.bot import handlers
import structlog

from telegram.ext import Updater, CommandHandler
from django.conf import settings


logger = structlog.get_logger("telegram_bot")


def main() -> None:
    """Run the bot."""

    logger.info("Starting bot...")

    updater = Updater(token=settings.TELEGRAMBOT_KEY, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handlers.start_command))

    dispatcher.add_handler(CommandHandler("unsubscribe", handlers.unsubscribe_command))

    dispatcher.add_handler(CommandHandler("subscribe", handlers.subscribe_command))

    updater.start_polling(
        timeout=10,
    )

    updater.idle()


if __name__ == "__main__":
    main()
