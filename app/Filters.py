from telegram import Message
from telegram.ext import filters

import re

from telegram.ext._utils.types import FilterDataDict


class FilterFullName(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        regex = r"[A-Za-zА-Яа-я-']{2,25}\s[A-Za-zА-Яа-я-']{2,25}(?:\s[A-Za-zА-Яа-я-']{2,25})?(?:\s[A-Za-zА-Яа-я-']{2,25})?(?:\s[A-Za-zА-Яа-я-']{4,6})?"

        matches = re.search(regex, message.text)

        return bool(matches)


filter_full_name = FilterFullName()


class FilterDOB(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        regex = r"^(\d{2})[.](\d{2})[.](\d{4})$"
        matches = re.search(regex, message.text)

        return bool(matches)


filter_dob = FilterDOB()


class FilterConfirmationCode(filters.MessageFilter):
    def filter(self, message: Message) -> bool:
        regex = r"^(\d{6})$"
        matches = re.search(regex, message.text)

        return bool(matches)


filter_confirmation_code = FilterConfirmationCode()
