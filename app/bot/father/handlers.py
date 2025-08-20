import logging

from telegram import Bot
from telegram.ext import CommandHandler, ContextTypes, MessageHandler

from app.database.models import Bot as BotModel
from app.database.models import StatusUser, WebhookUrl
from app.i18n import _
from app.settings import TG_SECRET_TOKEN
from app.utils.custom_update import Update
from app.utils.decorators import contextmanager
from app.utils.filters import Filter
from app.utils.helpers import get_bot

logger = logging.getLogger(__name__)


@contextmanager
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_html(
        text=_("Hi from bot father, send bot token to clone")
    )

    return StatusUser.WAIT_BOT_TOKEN


@contextmanager
async def clone_bot(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    try:
        token = update.message.text

        bot = await get_bot(token)

        if not update.db_session.get(BotModel, bot.id):
            new_clon = BotModel(
                id=bot.id,
                username=bot.username,
                name=bot.first_name,
                token=token,
                owner_id=update.effective_user.id,
            )
            update.db_session.add(new_clon)
            update.db_session.commit()

        webhook = update.db_session.get(WebhookUrl, 1)

        url = f"{webhook.url}/webhook/{bot.id}"

        await Bot(token).set_webhook(url=url, secret_token=TG_SECRET_TOKEN)

        await update.message.reply_html(text=_("Done"))

    except Exception as exc:
        logger.error(exc)

        await update.message.reply_html(text=_("Error"))

    return StatusUser.NONE


def handlers():

    return [
        CommandHandler("start", start),
        MessageHandler(Filter.status(StatusUser.WAIT_BOT_TOKEN), clone_bot),
    ]
