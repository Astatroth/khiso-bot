from app.StateManager import StateManager
from core.AppConfig import AppConfig
from core.Logger import Logger
from core.TranslationManager import TranslationManager
from kink import di, inject
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    ConversationHandler
)


@inject
class Application:
    def __init__(self, config: AppConfig, log: Logger, lang: TranslationManager):
        self.config = config
        self.log = log
        self.lang = lang
        self.state_manager = StateManager()

    async def error_handler(self, update: object, context: CallbackContext) -> int:
        self.log.error(msg=f"Exception while handling an update: {context.error}")

        if isinstance(update, Update):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=self.lang.t("errors.whoops")
            )

        return self.state_manager.get_end()

    def is_local(self) -> bool:
        return self.config.APP_ENV == "local"

    def run(self):
        application = ApplicationBuilder().token(self.config.BOT_TOKEN).build()

        conversation_handler = ConversationHandler(
            entry_points=self.state_manager.get_entry_points(),
            states=self.state_manager.get_states(),
            fallbacks=self.state_manager.get_fallbacks(),
            allow_reentry=True
        )
        application.add_handler(conversation_handler)

        application.add_error_handler(self.error_handler)

        if self.is_local():
            application.run_polling()
        else:
            application.run_webhook(
                listen=self.config.APP_IP,
                port=self.config.APP_PORT,
                url_path=self.config.BOT_URL,
                webhook_url=self.config.BOT_WEBHOOK_URL
            )
