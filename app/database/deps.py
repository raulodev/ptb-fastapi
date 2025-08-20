from contextlib import contextmanager
from typing import Annotated

from fastapi import Depends
from fastapi.security import APIKeyHeader
from sqlmodel import Session, SQLModel, create_engine, select

from app.database.models import Bot as BotModel
from app.settings import BOT_FATHER_TOKEN, DATABASE_URL
from app.utils.helpers import get_bot

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


async def init_db():
    with Session(engine) as session:
        bot_father = session.exec(
            select(BotModel).where(BotModel.token == BOT_FATHER_TOKEN)
        ).first()

        if not bot_father:
            bot_data = await get_bot(token=BOT_FATHER_TOKEN)

            bot_father = BotModel(
                id=bot_data.id,
                name=bot_data.first_name,
                username=bot_data.username,
                token=BOT_FATHER_TOKEN,
                is_father=True,
            )

            session.add(bot_father)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


api_key_scheme = APIKeyHeader(
    name="X-Telegram-Bot-Api-Secret-Token",
    scheme_name="Telegram Bot Api Secret Token",
    description="Tenant Api key",
)

ApiKeyDep = Annotated[str, Depends(api_key_scheme)]

SessionDep = Annotated[Session, Depends(get_session)]


dbsession = contextmanager(get_session)
