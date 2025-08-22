from app.bot.clon.handlers import handlers as clon_handlers
from app.bot.father.handlers import handlers as father_handlers
from app.database.deps import SessionDep
from app.database.models import Bot, User, UserContext
from app.utils.custom_update import Update
from app.utils.helpers import initialize_application


# pylint: disable=no-member
async def process_telegram_event(update_json: dict, session: SessionDep, bot: Bot):

    application = await initialize_application(bot.token)

    update = Update.de_json(update_json, application.bot)

    user_id = None
    first_name = None
    username = None

    if update.my_chat_member:
        user_id = update.my_chat_member.from_user.id
        first_name = update.my_chat_member.from_user.first_name
        username = update.my_chat_member.from_user.username

    elif update.effective_user:
        user_id = update.effective_user.id
        first_name = update.effective_user.first_name
        username = update.effective_user.username

    update.db_session = session

    if user_id:

        user = session.get(User, user_id)
        if not user:
            user = User(id=user_id, name=first_name, username=username)
            session.add(user)
            session.commit()

        ctxt = session.get(UserContext, user_id)
        if not ctxt:
            ctxt = UserContext(id=user_id, user_id=user_id, bot_id=bot.id)
            session.add(ctxt)
            session.commit()

        update.db_bot = bot
        update.db_user = user
        update.db_user_context = ctxt

    if bot.is_father:
        application.add_handlers(father_handlers())

    else:
        application.add_handlers(clon_handlers())

    await application.process_update(update)
