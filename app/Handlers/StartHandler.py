from app.Handlers.BaseHandler import BaseHandler
from kink import inject
from telegram import Update
from telegram.ext import CallbackContext


@inject
class StartHandler(BaseHandler):

    async def handle(self, update: Update, context: CallbackContext) -> int:
        await update.message.reply_text("Gerai")

        return self.end
