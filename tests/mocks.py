from unittest.mock import AsyncMock, MagicMock

from telegram import Bot, Update, User
from telegram.ext import CallbackContext

from app.database.models import Bot as BotModel
from app.database.models import StatusUser
from app.database.models import User as UserModel
from app.database.models import UserContext

mock_tg_user = MagicMock(spec=User)
mock_tg_user.id = 1
mock_tg_user.first_name = "Raul"
mock_tg_user.username = "raul"
mock_tg_user.is_bot = False

mock_tg_user_bot = MagicMock(spec=User)
mock_tg_user_bot.id = 1
mock_tg_user_bot.first_name = "Bot"
mock_tg_user_bot.username = "bot"
mock_tg_user_bot.is_bot = True

mock_tg_bot = MagicMock(spec=Bot)
mock_tg_bot.bot = mock_tg_user_bot
mock_tg_bot.id = mock_tg_user_bot.id
mock_tg_bot.first_name = mock_tg_user_bot.first_name
mock_tg_bot.username = mock_tg_user_bot.username
mock_tg_bot.token = "token"
mock_tg_bot.send_message = AsyncMock()

mock_tg_callback_context = MagicMock(spec=CallbackContext)
mock_tg_callback_context.bot = mock_tg_bot


mock_db_bot = MagicMock(spec=BotModel)
mock_db_bot.id = 1
mock_db_bot.token = "token"
mock_db_bot.is_father = False
mock_db_bot.is_active = True

mock_db_user = MagicMock(spec=UserModel)
mock_db_user.id = 1
mock_db_user.name = "Raul"
mock_db_user.username = "raul"
mock_db_user.is_superuser = False

mock_db_user_context = MagicMock(spec=UserContext)
mock_db_user_context.user = mock_db_user
mock_db_user_context.bot = mock_db_bot
mock_db_user_context.is_owner = False
mock_db_user_context.is_admin = False
mock_db_user_context.status = StatusUser.NONE


mock_tg_update = MagicMock(spec=Update)
mock_tg_update.my_chat_member = None
mock_tg_update.effective_user = mock_tg_user
mock_tg_update.message.reply_html = AsyncMock()
mock_tg_update.callback_query.answer = AsyncMock()
mock_tg_update.callback_query.message.edit_reply_markup = AsyncMock()
mock_tg_update.callback_query.message.reply_text = AsyncMock()
mock_tg_update.db_user = mock_db_user
mock_tg_update.db_user_context = mock_db_user_context
