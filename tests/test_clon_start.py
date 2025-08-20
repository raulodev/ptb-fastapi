import pytest

from app.bot.clon.handlers import start
from app.i18n import _
from tests.mocks import mock_tg_callback_context, mock_tg_update


@pytest.mark.asyncio
async def test_clon_start_command():

    await start(mock_tg_update, mock_tg_callback_context)

    assert mock_tg_update.message.reply_html.call_count == 1
    mock_tg_update.message.reply_html.assert_called_with(text=_("Hi from bot clon"))
