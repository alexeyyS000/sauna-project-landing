from telegram import Update
from telegram.ext import CallbackContext


def start_command(update: Update, context: CallbackContext) -> None:
    """Handle the /start command."""
    update.message.reply_text("Hello! I'm your bot.")
