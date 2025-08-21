from sqlmodel import Session
from telegram import Update as TgUpdate

from app.database.models import Bot, User, UserContext


class Update(TgUpdate):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.db_bot: Bot | None = None
        self.db_user: User | None = None
        self.db_user_context: UserContext | None = None
        self.db_session: Session | None = None

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
