from app.Handlers.CommandHanlder import CommandHandler as CHandler
from app.Handlers.StartHandler import StartHandler
from telegram.ext import (
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from typing import Dict, List


class StateManager:

    def __init__(self):
        self.command_handler = CHandler(self.get_end())
        self.start_handler = StartHandler(self.get_end())

    def get_end(self) -> int:
        return ConversationHandler.END

    def get_entry_points(self) -> List:
        return [
            CommandHandler('start', self.command_handler.handle_start)
        ]

    def get_fallbacks(self) -> List:
        return [
            CommandHandler('stop', self.command_handler.handle_stop)
        ]

    def get_states(self) -> Dict:
        return {
            1: [MessageHandler(filters.ALL, self.start_handler.handle)]
        }
