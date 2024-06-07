from app.Filters import FilterName, FilterDOB, FilterConfirmationCode
from app.Handlers.CommandHanlder import CommandHandler as CHandler
from app.Handlers.Controller import Controller
from app.State import State
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
)
from typing import Dict, List


class StateManager:

    def __init__(self):
        self.command_handler = CHandler(self.get_end())
        self.controller = Controller(self.get_end())

    def get_end(self) -> int:
        return ConversationHandler.END

    def get_entry_points(self) -> List:
        return [
            CommandHandler('start', self.controller.start)
        ]

    def get_fallbacks(self) -> List:
        return [
            CommandHandler('stop', self.command_handler.handle_stop)
        ]

    def get_states(self) -> Dict:
        filter_name = FilterName()
        filter_dob = FilterDOB()
        filter_confirmation_code = FilterConfirmationCode()

        return {
            State.SET_LANGUAGE: [CallbackQueryHandler(self.controller.set_language, pattern='^uz|ru$')],
            State.AWAIT_SUBSCRIPTION: [
                CallbackQueryHandler(self.controller.check_subscription, pattern='^check_subscription$')
            ],
            State.AWAIT_CONTACT: [MessageHandler(filters.CONTACT, self.controller.set_phone_number)],
            State.AWAIT_NAME: [MessageHandler(filter_name, self.controller.set_full_name)],
            State.AWAIT_DATE_OF_BIRTH: [MessageHandler(filter_dob, self.controller.set_date_of_birth)],
            State.AWAIT_GENDER: [CallbackQueryHandler(self.controller.set_gender, pattern='^gender_[1-2]$')],
            State.AWAIT_REGION: [
                CallbackQueryHandler(self.controller.set_region, pattern='^region_[0-9]+$'),
                CallbackQueryHandler(self.controller.set_region, pattern='^prev_[0-9]+|next_[0-9]+$')

            ],
            State.AWAIT_DISTRICT: [
                CallbackQueryHandler(self.controller.set_district, pattern='^district_[0-9]+$'),
                CallbackQueryHandler(self.controller.set_district, pattern='^prev_[0-9]+|next_[0-9]+$'),
                CallbackQueryHandler(self.controller.set_district, pattern='^back+$')
            ],
            State.AWAIT_INSTITUTION: [
                CallbackQueryHandler(self.controller.set_institution, pattern='^institution_[0-9]+$'),
                CallbackQueryHandler(self.controller.set_institution, pattern='^prev_[0-9]+|next_[0-9]+$'),
                CallbackQueryHandler(self.controller.set_institution, pattern='^back+$')
            ],
            State.AWAIT_GRADE: [CallbackQueryHandler(self.controller.set_grade, pattern='^grade_[0-9]+$')],
            State.VALIDATE_CODE: [MessageHandler(filter_confirmation_code, self.controller.validate_confirmation_code)],
            State.IDLE: [MessageHandler(filters.ALL, self.controller.idle)]
        }
