from app.Handlers.BaseHandler import BaseHandler
from kink import inject
from telegram import Update
from telegram.ext import CallbackContext


@inject
class CommandHandler(BaseHandler):

    async def handle_start(self, update: Update, context: CallbackContext) -> int:
        return 1

    async def handle_stop(self, update: Update, context: CallbackContext) -> int:
        self.logger.info("Stopping bot")

        return self.end
