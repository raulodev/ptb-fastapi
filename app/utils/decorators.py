import logging
from functools import wraps

from telegram.ext import CallbackContext

from app.i18n import _
from app.utils.custom_update import Update

logger = logging.getLogger(__name__)


def contextmanager(_func=None, only_admin=False):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: CallbackContext, *args, **kwargs):

            user = update.db_user
            ctxt = update.db_user_context

            is_authorized = ctxt.is_admin or ctxt.is_owner or user.is_superuser

            if only_admin and not is_authorized:

                text = _("You are not authorized")

                if update.callback_query:
                    await update.callback_query.answer(text, show_alert=True)

                elif update.message:
                    await update.message.reply_text(text)

                return

            status = await func(update, context, *args, **kwargs)

            if status:
                logger.debug("New status: %s", status)
                ctxt.status = status
                update.db_session.commit()

        return wrapper

    if _func is not None:
        return decorator(_func)

    return decorator
