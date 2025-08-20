import logging

from async_lru import alru_cache
from telegram import Bot
from telegram.ext import Application, ExtBot

logger = logging.getLogger(__name__)


@alru_cache
async def get_bot(token: str):
    """Fetch bot info from telegram"""
    logger.info("Fetching bot info for %s", token)
    data = await Bot(token=token).get_me()
    return data


@alru_cache
async def initialize_application(token: str):
    # pylint: disable=protected-access

    application = Application.builder().token(token).updater(None).build()
    bot_user = await get_bot(token)
    logger.info("Initializing application for %s", bot_user.username)
    bot_user._bot._initialized = True
    extbot = ExtBot(token=token)
    extbot._bot_user = bot_user
    extbot._initialized = True
    application._initialized = True
    application.bot = extbot
    return application
