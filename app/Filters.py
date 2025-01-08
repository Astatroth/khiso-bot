from telegram import Message
from telegram.ext import filters

import re

from telegram.ext._utils.types import FilterDataDict


class FilterName(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        regex = r"[A-Za-zА-Яа-я-]{2,25}\s[A-Za-zА-Яа-я-]{2,25}"
        matches = re.search(regex, message.text)

        return True if matches else False


class FilterDOB(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        regex = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(\d{4})$"
        matches = re.search(regex, message.text)

        return True if matches else False


class FilterConfirmationCode(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        if not message.text:
            return False

        regex = r"^(\d{6})$"
        matches = re.search(regex, message.text)

        return True if matches else False
