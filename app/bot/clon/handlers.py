from telegram.ext import CommandHandler, ContextTypes

from app.i18n import _
from app.utils.custom_update import Update
from app.utils.decorators import contextmanager


@contextmanager
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_html(text=_("Hi from bot clon"))


def handlers():
    return [
        CommandHandler("start", start),
    ]
