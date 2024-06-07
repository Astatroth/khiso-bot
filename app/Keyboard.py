from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from typing import Dict, List, Union


class Keyboard:
    @staticmethod
    def button(text: str, request_contact: bool = False) -> KeyboardButton:
        return KeyboardButton(text, request_contact=request_contact)

    @staticmethod
    def inline(buttons: List, cols: int = 2):
        keyboard = []
        for text, data in buttons:
            keyboard.append(InlineKeyboardButton(text, callback_data=data))

        keyboard = [keyboard[i:i + cols] for i in range(0, len(buttons), cols)]

        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def inline_button(text: str, callback_data: str) -> InlineKeyboardButton:
        return InlineKeyboardButton(text, callback_data=callback_data)

    @staticmethod
    def reply(buttons: List, resize_keyboard: bool = False, one_time_keyboard: bool = False) -> ReplyKeyboardMarkup:
        keyboard = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]

        return ReplyKeyboardMarkup(keyboard, resize_keyboard=resize_keyboard, one_time_keyboard=one_time_keyboard)
