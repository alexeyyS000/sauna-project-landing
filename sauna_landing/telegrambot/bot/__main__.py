import logging

from telegram.ext import Updater, CommandHandler

from sauna_landing.sauna_landing.settings import TELEGRAMBOT_KEY

from .handlers import start_command


def main() -> None:
    """Run the bot."""

    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )
    logger = logging.getLogger(__name__)

    updater = Updater(token=TELEGRAMBOT_KEY, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_command))

    updater.start_polling(
        timeout=10,
    )

    updater.idle()


if __name__ == "__main__":
    main()
