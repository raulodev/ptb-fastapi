from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class StatusUser(str, Enum):
    NONE = "NONE"
    WAIT_BOT_TOKEN = "WAIT_BOT_TOKEN"


class CreatedUpdatedFields(SQLModel):
    created: datetime = Field(default=datetime.now(tz=timezone.utc), nullable=False)
    updated: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
        nullable=False,
    )


class WebhookUrl(CreatedUpdatedFields, table=True):
    id: int | None = Field(default=None, primary_key=True)
    url: str


class Bot(CreatedUpdatedFields, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    username: str = Field(index=True)
    token: str
    is_active: bool = Field(default=True)
    is_father: bool = Field(default=False)
    owner_id: int | None = Field(default=None, foreign_key="user.id")


class User(CreatedUpdatedFields, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    username: str = Field(index=True)
    is_superuser: bool = Field(default=False)


class UserContext(CreatedUpdatedFields, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    bot_id: int = Field(foreign_key="bot.id")
    status: StatusUser = Field(default=StatusUser.NONE)
    is_admin: bool = Field(default=False)
    is_owner: bool = Field(default=False)
