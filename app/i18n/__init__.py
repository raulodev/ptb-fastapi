import gettext
import logging
from pathlib import Path

from app.settings import LANGUAGE_CODE

logger = logging.getLogger(__name__)


class TranslationWrapper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.init_translation()
        return cls._instance

    def init_translation(self):
        locales_dir = Path(__file__).parent / "translations"
        self.translations = gettext.translation(
            "messages", localedir=locales_dir, languages=[LANGUAGE_CODE], fallback=True
        )
        self.translations.install()

    def gettext(self, message: str) -> str:
        return self.translations.gettext(message)


async def set_locale(lang: str):
    translation_wrapper = TranslationWrapper()

    locales_dir = Path(__file__).parent.parent / "translations"

    # pylint: disable=:attribute-defined-outside-init
    translation_wrapper.translations = gettext.translation(
        "messages", localedir=locales_dir, languages=[lang], fallback=True
    )

    translation_wrapper.translations.install()


def _(message: str) -> str:
    """
    Get the translated string for the specified message.

    This method is a shorthand for calling gettext() and
    is used to retrieve translated strings.

    Args:
        message (str): The message to be translated.

    Returns:
        str: The translated string.
    """
    translation_wrapper = TranslationWrapper()
    return translation_wrapper.gettext(message)
