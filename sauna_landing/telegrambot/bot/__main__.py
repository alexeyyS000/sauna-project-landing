import django

django.setup()

import structlog
import redis
from telegram.ext import Updater, CommandHandler, Dispatcher, PicklePersistence
from django.conf import settings
from . import handlers

logger = structlog.get_logger("telegram_bot")


def main() -> None:
    """Run the bot with Redis persistence."""

    logger.info("Starting bot...")


    redis_client = redis.StrictRedis(
        host=settings.REDIS_BOT_HOST,
        port=settings.REDIS_BOT_PORT,
        db=0,
        decode_responses=False
    )


    persistence = PicklePersistence(filename="bot_data.pkl")
    persistence.redis_client = redis_client


    updater = Updater(token=settings.TELEGRAMBOT_KEY, use_context=True, persistence=persistence)

    dispatcher: Dispatcher = updater.dispatcher


    dispatcher.add_handler(CommandHandler("start", handlers.start))


    updater.start_polling(timeout=10)
    updater.idle()


if __name__ == "__main__":
    main()
