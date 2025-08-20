from telegram.ext.filters import UpdateFilter

from app.utils.custom_update import Update


class Filter:

    class status(UpdateFilter):
        __slots__ = ("status", "filter_status")

        def __init__(self, filter_status: str):
            self.filter_status = filter_status
            super().__init__("Filters.status", None)

        def filter(self, update: Update) -> bool:

            return update.db_user_context.status == self.filter_status
