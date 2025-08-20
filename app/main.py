import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from sqlmodel import select
from telegram import Bot
from telegram.error import BadRequest, InvalidToken, TimedOut

from app.bot.dispatcher import process_telegram_event
from app.database.deps import ApiKeyDep, SessionDep, create_db_and_tables, init_db
from app.database.models import Bot as BotModel
from app.database.models import WebhookUrl
from app.i18n import set_locale
from app.settings import TG_SECRET_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


class Url(BaseModel):
    url: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    await init_db()
    yield


app = FastAPI(title="Ptb fastapi template", lifespan=lifespan)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):

    if (
        request.method == "POST"
        and request.url.path != "/setWebhook"
        and request.headers.get("X-Telegram-Bot-Api-Secret-Token") == TG_SECRET_TOKEN
    ):

        update = await request.json()
        language_code = update.get("message", {}).get("from", {}).get("language_code")

        logger.info("Language code: %s", language_code)
        await set_locale(language_code)

    response = await call_next(request)
    return response


@app.post("/webhook/{bot_id}", tags=["Process Telegram Updates"])
async def webhook(
    bot_id: int, request: Request, api_key: ApiKeyDep, session: SessionDep
):
    if api_key == TG_SECRET_TOKEN:
        update_json = await request.json()
        logging.info(update_json)
        try:
            bot = session.get(BotModel, bot_id)
            if bot:
                await process_telegram_event(update_json, session, bot)
        except TimedOut:
            logger.error("Timed out")
    return {"message": "ok"}


@app.post("/setWebhook", tags=["Set bot webhook"])
async def set_webhook(data: Url, session: SessionDep, api_key: ApiKeyDep):
    """Use this method to specify a url and
    receive incoming updates via an outgoing webhook.
    """

    if api_key == TG_SECRET_TOKEN:
        try:

            webhook_url = session.get(WebhookUrl, 1)
            if not webhook_url:
                webhook_url = WebhookUrl(url=data.url)
                session.add(webhook_url)
                session.commit()
            else:
                webhook_url.url = data.url
                session.commit()

            bots = session.exec(select(BotModel)).all()

            for bot in bots:

                await Bot(bot.token).set_webhook(
                    url=f"{data.url}/webhook/{bot.id}",
                    secret_token=TG_SECRET_TOKEN,
                )
            return {"message": "ok"}
        except (InvalidToken, BadRequest, TimedOut) as exc:
            raise HTTPException(status_code=400, detail=exc.message) from exc
    raise HTTPException(status_code=400, detail="bad requests")
