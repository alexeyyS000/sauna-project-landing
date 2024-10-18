from telegram import Update
from telegram.ext import CallbackContext
import structlog

logger = structlog.get_logger("telegram_bot")

def start_command(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""

    logger.info("Received /start command", user_id=1, username='test')

    update.message.reply_text("Hello! I'm your bot.")
