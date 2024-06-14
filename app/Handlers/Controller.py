import random
import telegram.error

from app.Classes.Olympiad import Olympiad
from app.Classes.Student import Student
from app.Classes.Sms import Sms
from app.Handlers.BaseHandler import BaseHandler
from app.Keyboard import Keyboard
from app.State import State
from app.helpers import sanitize
from kink import inject
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

import flag


@inject
class Controller(BaseHandler):
    async def start(self, update: Update, context: CallbackContext) -> int:
        """ Start command handler """
        student = Student(update.message.chat.id)
        student.authenticate()

        if not student.is_authenticated():
            return await self.select_language(update)

        context.user_data['student'] = student
        self.i18n.set_locale(student.language)

        return await self.greet(update, context)

    async def select_language(self, update: Update) -> int:
        """ Show an inline keyboard for language selection """
        await update.message.reply_text(
            "Tilni tanlang / Выберите язык",
            reply_markup=Keyboard.inline([
                ("{} O'zbek".format(flag.flag('uz')), "uz"),
                ("{} Русский".format(flag.flag('ru')), "ru")
            ])
        )
        return State.SET_LANGUAGE

    async def set_language(self, update: Update, context: CallbackContext) -> int:
        """ Set the language for the current user """
        context.user_data['language'] = update.callback_query.data
        self.i18n.set_locale(update.callback_query.data)

        await update.callback_query.answer()
        await update.callback_query.message.delete()

        return await self.request_contact(update, context)

    async def demand_subscription(self, update: Update, context: CallbackContext) ->int:
        """ Demand the user to subscribe to listed channels in order to continue """
        from app.Classes.Subscription import Subscription

        context.user_data['is_subscribed'] = 0
        channels = Subscription().get_subscriptions()
        if len(channels) == 0:
            return await self.request_name(update, context)

        buttons = []
        for channel in channels:
            buttons.append((f"{channel.get('title')}", channel.get('url')))

        buttons.append(("\U0001F44D " + self.i18n.t("strings.confirm_subscription"), "check_subscription"))

        await update.message.chat.send_message(
            "\u274C " + sanitize(self.i18n.t("strings.demand_subscription")),
            parse_mode=ParseMode.MARKDOWN_V2,
            reply_markup=Keyboard.inline_url(buttons)
        )

        return State.AWAIT_SUBSCRIPTION

    async def check_subscription(self, update: Update, context: CallbackContext) -> int:
        """ Check if the user have subscribed to channels """
        from app.Classes.Subscription import Subscription

        channels = Subscription().get_subscriptions()
        if len(channels) == 0:
            return await self.request_name(update, context)

        subscribed_channels = 0
        statuses = [
            telegram.ChatMember.MEMBER,
            telegram.ChatMember.OWNER,
            telegram.ChatMember.ADMINISTRATOR,
        ]
        for channel in channels:
            channel_id = channel.get("channel_id")

            try:
                user = await update.get_bot().get_chat_member(
                    chat_id=channel_id,
                    user_id=update.callback_query.message.chat.id
                )
                if user.status in statuses:
                    subscribed_channels += 1
            except telegram.error.BadRequest:
                pass

        if subscribed_channels < len(channels):
            await update.callback_query.answer(text=self.i18n.t("strings.not_subscribed"))
            return State.AWAIT_SUBSCRIPTION

        await update.callback_query.message.delete()

        context.user_data['is_subscribed'] = 1

        return await self.request_name(update, context)

    async def request_contact(self, update: Update, context: CallbackContext) -> int:
        """ Display "Share contact" button"""
        await update.callback_query.message.chat.send_message(
            self.i18n.t("strings.share_your_contact"),
            reply_markup=Keyboard.reply(
                [Keyboard.button(text=self.i18n.t("strings.share_contact"), request_contact=True)],
                resize_keyboard=True,
                one_time_keyboard=True
            )
        )

        return State.AWAIT_CONTACT

    async def set_phone_number(self, update: Update, context: CallbackContext) -> int:
        """ Set the phone number for the current user """
        context.user_data['phone_number'] = update.message.contact.phone_number

        return await self.request_confirmation_code(update, context)

    async def request_name(self, update: Update, context: CallbackContext) -> int:
        """ Ask the user for his first name and last name """
        await update.callback_query.message.chat.send_message(self.i18n.t("strings.enter_full_name"), reply_markup=None)

        return State.AWAIT_NAME

    async def set_full_name(self, update: Update, context: CallbackContext) -> int:
        """ Set the full name for the current user """
        context.user_data['full_name'] = update.message.text

        return await self.request_date_of_birth(update, context)

    async def request_date_of_birth(self, update: Update, context: CallbackContext) -> int:
        """ Ask the user for his date of birth """
        await update.message.reply_text(self.i18n.t("strings.enter_date_of_birth"))

        return State.AWAIT_DATE_OF_BIRTH

    async def set_date_of_birth(self, update: Update, context: CallbackContext) -> int:
        """ Set the date of birth for the current user """
        context.user_data['date_of_birth'] = Student.clean_date_of_birth(update.message.text)

        return await self.request_gender(update, context)

    async def request_gender(self, update: Update, context: CallbackContext) -> int:
        """ Request gender from the user """
        await update.message.reply_text(
            self.i18n.t("strings.select_gender"),
            reply_markup=Keyboard.inline([
                (self.i18n.t("strings.gender_female"), "gender_{}".format(Student.GENDER_FEMALE)),
                (self.i18n.t("strings.gender_male"), "gender_{}".format(Student.GENDER_MALE))
            ])
        )

        return State.AWAIT_GENDER

    async def set_gender(self, update: Update, context: CallbackContext) -> int:
        """ Set the gender for the current user """
        command, value = update.callback_query.data.split('_')
        context.user_data['gender'] = int(value)

        await update.callback_query.answer()
        await update.callback_query.edit_message_reply_markup(reply_markup=None)
        await update.callback_query.message.delete()

        return await self.request_region(update, context)

    async def request_region(self, update: Update, context: CallbackContext) -> int:
        """ Display paginated navigation through regions, request the user to choose one """
        from app.Classes.Region import Region

        regions = Region().get_regions(12)
        if update.message is not None:
            """await update.message.reply_text(
                self.i18n.t("strings.select_region"),
                reply_markup=Keyboard.inline(regions)
            )"""
            await update.callback_query.edit_message_text(
                self.i18n.t("strings.select_region")
            )
            await update.callback_query.edit_message_reply_markup(
                Keyboard.inline(regions)
            )
        else:
            await update.callback_query.message.chat.send_message(
                self.i18n.t("strings.select_region"),
                reply_markup=Keyboard.inline(regions)
            )

        return State.AWAIT_REGION

    async def set_region(self, update: Update, context: CallbackContext) -> int:
        """ Set region for the current user """
        from app.Classes.Region import Region

        command, value = update.callback_query.data.split('_')
        if command in ["prev", "next"]:
            await update.callback_query.answer()
            page = int(value) - 1 if command == "prev" else int(value) + 1
            regions = Region().get_regions(12, page=page)
            await update.callback_query.edit_message_reply_markup(Keyboard.inline(regions))

            return State.AWAIT_REGION

        await update.callback_query.answer()
        context.user_data["region_id"] = int(value)

        return await self.request_district(update, context)

    async def request_district(self, update: Update, context: CallbackContext) -> int:
        """ Display districts list from the selected region and request the user to choose one """
        from app.Classes.District import District

        districts = District().get_districts(context.user_data.get("region_id"), 12)
        await update.callback_query.edit_message_text(
            self.i18n.t("strings.select_district")
        )
        await update.callback_query.edit_message_reply_markup(
            Keyboard.inline(districts)
        )

        return State.AWAIT_DISTRICT

    async def set_district(self, update: Update, context: CallbackContext) -> int:
        """
            Handle callback command
            Redirect to region select on 'back'
            Set the district_id for the current user
        """
        from app.Classes.District import District

        # Handle 'back' command
        if update.callback_query.data == "back":
            await update.callback_query.answer()
            await update.callback_query.message.delete()
            return await self.request_region(update, context)

        # Handle other commands
        command, value = update.callback_query.data.split('_')
        if command in ["prev", "next"]:
            await update.callback_query.answer()
            page = int(value) - 1 if command == "prev" else int(value) + 1
            districts = District().get_districts(context.user_data.get("region_id"), 12, page=page)
            await update.callback_query.edit_message_reply_markup(Keyboard.inline(districts))

            return State.AWAIT_DISTRICT

        await update.callback_query.answer()
        context.user_data['district_id'] = int(value)

        return await self.request_institution(update, context)

    async def request_institution(self, update: Update, context: CallbackContext) -> int:
        """
            Display paginated institutions list for the selected region and district
            Requests the user to choose one
        """
        from app.Classes.Institution import Institution

        institutions = Institution().get_institutions(context.user_data.get("district_id"), 12)
        await update.callback_query.edit_message_text(
            self.i18n.t("strings.select_institution")
        )
        await update.callback_query.edit_message_reply_markup(
            Keyboard.inline(institutions)
        )

        return State.AWAIT_INSTITUTION

    async def set_institution(self, update: Update, context: CallbackContext) -> int:
        """
            Handle callback command
            Redirect to district select on 'back'
            Set the institution_id for the current user
        """
        from app.Classes.Institution import Institution

        # Handle 'back' command
        if update.callback_query.data == "back":
            await update.callback_query.answer()
            # await update.callback_query.message.delete()
            return await self.request_district(update, context)

        # Handle other commands
        command, value = update.callback_query.data.split('_')
        if command in ["prev", "next"]:
            await update.callback_query.answer()
            page = int(value) - 1 if command == "prev" else int(value) + 1
            institutions = Institution().get_institutions(context.user_data.get("district_id"), 12, page=page)
            await update.callback_query.edit_message_reply_markup(Keyboard.inline(institutions))

            return State.AWAIT_INSTITUTION

        await update.callback_query.answer()
        context.user_data['institution_id'] = int(value)

        return await self.request_grade(update, context)

    async def request_grade(self, update: Update, context: CallbackContext) -> int:
        """ Request the grade from the user """

        keyboard = []
        for grade in range(1, 12):
            keyboard.append(
                (
                    str(grade), "grade_{}".format(grade)
                )
            )

        await update.callback_query.edit_message_text(
            self.i18n.t("strings.select_grade")
        )
        await update.callback_query.edit_message_reply_markup(
            Keyboard.inline(keyboard, cols=6)
        )

        return State.AWAIT_GRADE

    async def set_grade(self, update: Update, context: CallbackContext) -> int:
        """ Set the grade for the current user """
        command, grade = update.callback_query.data.split("_")
        context.user_data['grade'] = int(grade)

        student = Student(update.callback_query.message.chat.id)
        student.register(context.user_data)
        student.authenticate()
        context.user_data["student"] = student

        await update.callback_query.answer()
        await update.callback_query.message.delete()

        return await self.greet(update, context)

    async def request_confirmation_code(self, update: Update, context: CallbackContext) -> int:
        """ Send SMS with a confirmation code and request it from the user """

        Sms().send_code(context.user_data.get("phone_number"), context.user_data.get("language"))

        await update.message.chat.send_message(
            self.i18n.t("strings.confirmation_code_sent") + "\r\n\r\n" + self.i18n.t("strings.enter_confirmation_code")
        )

        return State.VALIDATE_CODE

    async def validate_confirmation_code(self, update: Update, context: CallbackContext) -> int:
        """ Validate the confirmation code """
        code = update.message.text
        code = Sms().validate_code(context.user_data.get("phone_number"), code, context.user_data.get("language"))

        if code.get("code") is False:
            await update.message.reply_text(self.i18n.t("confirmation_code_incorrect"))
            return State.VALIDATE_CODE

        context.user_data["is_verified"] = 1

        return await self.demand_subscription(update, context)

    async def greet(self, update: Update, context: CallbackContext) -> int:
        """ Greet the user """

        if update.message is None:
            await update.callback_query.message.chat.send_message(
                self.i18n.t("strings.greet").format(sanitize(context.user_data.get("student").full_name))
            )
        else:
            await update.message.reply_text(
                self.i18n.t("strings.greet").format(sanitize(context.user_data.get("student").full_name))
            )

        return State.IDLE

    async def idle(self, update: Update, context: CallbackContext):
        message = update.message
        query = update.callback_query
        student = context.user_data["student"]

        if query is not None:
            command, value = query.data.split("_")

            match command:
                case "signup":
                    # Try to sign up to olympiad
                    response = student.signup(value)
                    if response is None:
                        await update.callback_query.edit_message_reply_markup(reply_markup=None)
                        await update.callback_query.message.reply_text(self.i18n.t("errors.whoops"))
                        await update.callback_query.answer()

                        return State.IDLE
                    else:
                        status = response.get("status")
                        if status == 0:
                            await update.callback_query.edit_message_reply_markup(reply_markup=None)
                            await update.callback_query.message.reply_text(response.get("error")["message"])
                            await update.callback_query.answer()
                        else:
                            await update.callback_query.edit_message_reply_markup(reply_markup=None)
                            await update.callback_query.message.reply_text(self.i18n.t("strings.sign_up_success"))
                            await update.callback_query.answer()

                        return State.IDLE
                case "start":
                    context.user_data["question_number"] = 1
                    response = Olympiad().start(value, context.user_data.get("student").id)

                    if response is None:
                        await update.callback_query.edit_message_reply_markup(reply_markup=None)
                        await update.callback_query.message.reply_text(self.i18n.t("errors.whoops"))
                        await update.callback_query.answer()

                        return State.IDLE
                    else:
                        status = response.get("status")
                        if status == 0:
                            await update.callback_query.edit_message_reply_markup(reply_markup=None)
                            await update.callback_query.message.reply_text(response.get("error")["message"])
                            await update.callback_query.answer()

                            return State.IDLE

                        context.user_data["olympiad_id"] = value
                        await update.callback_query.answer(response.get("message"))
                        await update.callback_query.edit_message_reply_markup(reply_markup=None)

                        return await self.request_question(update, context)
                case _:
                    await update.callback_query.edit_message_reply_markup(reply_markup=None)

        return State.IDLE

    async def request_question(self, update: Update, context: CallbackContext) -> int:
        if context.user_data.get("question_number") is None:
            context.user_data["question_number"] = 1

        response = Olympiad().get_question(
            context.user_data.get("olympiad_id"),
            context.user_data.get("student").id,
            context.user_data.get("question_number")
        )

        if response.get("status") == 0:
            await update.callback_query.message.chat.send_message(response.get("error")["message"])

            return State.IDLE

        question = response.get("question")
        question_type = question["type_label"]
        buttons = []

        for answer in list(question["answers"]):
            buttons.append((answer["answer"], "answer_{}_{}".format(answer["question_id"], answer["id"])))

        random.shuffle(buttons)

        match question_type:
            case "Image":
                await update.callback_query.message.chat.send_photo(
                    photo=question["content"],
                    caption=self.i18n.t("strings.question").format(context.user_data["question_number"]),
                    reply_markup=Keyboard.inline(buttons, 1)
                )
            case "Document":
                await update.callback_query.message.chat.send_document(
                    document=question["content"],
                    caption=self.i18n.t("strings.question").format(context.user_data["question_number"]),
                    reply_markup=Keyboard.inline(buttons, 1)
                )
            case _:
                await update.callback_query.message.chat.send_message(
                    text=self.i18n.t("strings.question").format(context.user_data["question_number"]) + "\r\n\r\n" + question["content"],
                    reply_markup=Keyboard.inline(buttons, 1)
                )

        return State.AWAIT_ANSWER

    async def accept_answer(self, update: Update, context: CallbackContext) -> int:
        answer = update.callback_query.data
        command, question_id, answer_id = answer.split("_")

        response = Olympiad().send_answer(
            question_id,
            answer_id,
            context.user_data.get("student").id
        )

        if response.get("status") == 0:
            await update.callback_query.answer()
            await update.callback_query.message.delete()
            await update.callback_query.message.chat.send_message(response.get("error")["message"])

            return State.IDLE

        await update.callback_query.answer(self.i18n.t("strings.answer_accepted"))
        await update.callback_query.message.delete()

        context.user_data["question_number"] += 1

        return await self.request_question(update, context)
