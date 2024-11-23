
import re


from telegram import Message

from telegram.ext.filters import MessageFilter


NAME_FILTER_PATTERN = re.compile(r'^[a-zA-Zа-яА-ЯёЁ]{1,20}$')


class IsValidNameFilter(MessageFilter):
    def filter(self, message: Message):
        text = message.text
        if text is not None:
            return bool(re.match(NAME_FILTER_PATTERN, text))
        else:
            return False


IS_VALID_NAME_FILTER = IsValidNameFilter()