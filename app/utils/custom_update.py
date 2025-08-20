from sqlmodel import Session
from telegram import Update as TgUpdate

from app.database.models import Bot, User, UserContext


class Update(TgUpdate):

    db_bot = Bot
    db_user = User
    db_user_context = UserContext
    db_session: Session

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
