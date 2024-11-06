import django

django.setup()

import structlog

from telegram.ext import Updater, CommandHandler
from django.conf import settings
from .handlers import start_command

logger = structlog.get_logger("telegram_bot")


def main() -> None:
    """Run the bot."""

    logger.info("Starting bot...")

    updater = Updater(token=settings.TELEGRAMBOT_KEY, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))

    updater.start_polling(
        timeout=10,
    )

    updater.idle()


if __name__ == "__main__":
    main()
