import django

django.setup()
from telegrambot.bot import handlers
import structlog

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from django.conf import settings


logger = structlog.get_logger("telegram_bot")

bot_instance = None


def main() -> None:
    """Run the bot."""
    global bot_instance

    logger.info("Starting bot...")

    updater = Updater(token=settings.TELEGRAMBOT_KEY, use_context=True)
    bot_instance = updater.bot

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", handlers.start_command))

    dispatcher.add_handler(CommandHandler("unsubscribe", handlers.unsubscribe_command))

    dispatcher.add_handler(CommandHandler("subscribe", handlers.subscribe_command))

    dispatcher.add_handler(CallbackQueryHandler(handlers.handle_button_click))

    dispatcher.add_handler(CommandHandler("start2", handlers.start2))

    dispatcher.add_handler(CallbackQueryHandler(handlers.button))

    updater.start_polling(
        timeout=10,
    )

    updater.idle()


if __name__ == "__main__":
    main()
