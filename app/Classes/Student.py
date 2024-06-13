from core.API import API
from core.Logger import Logger
from functools import wraps
from kink import inject

import re


@inject
class Student:
    GENDER_FEMALE = 1
    GENDER_MALE = 2

    def __init__(self, chat_id: int, api: API, logger: Logger):
        self.id = None
        self.chat_id = chat_id
        self.user_id = None
        self.language = None
        self.first_name = None
        self.last_name = None
        self.full_name = None
        self.phone_number = None

        self.api = api
        self.logger = logger

    def authenticate(self) -> None:
        response = self.api.get(f"students/{self.chat_id}")
        self.logger.info(response)
        student = response.get("student")

        if student is not None:
            self.id = student.get("id")
            self.user_id = student.get("user_id")
            self.language = student.get("language")
            self.first_name = student.get("first_name")
            self.last_name = student.get("last_name")
            self.full_name = student.get("full_name")
            self.phone_number = student.get("phone_number")

    @staticmethod
    def clean_date_of_birth(date_of_birth: str) -> str:
        regex = r"(\d{2})[/.](\d{2})[/.](\d{4})"
        matches = re.search(regex, date_of_birth)

        return '.'.join(str(i) for i in matches.groups())

    def is_authenticated(self) -> bool:
        return self.user_id is not None and self.language is not None

    def register(self, data: dict):
        self.api.put("students/create", {
            "chat_id": self.chat_id,
            "phone_number": data.get("phone_number"),
            "full_name": data.get("full_name"),
            "gender": data.get("gender"),
            "date_of_birth": data.get("date_of_birth"),
            "language": data.get("language"),
            "is_verified": data.get("is_verified"),
            "is_subscribed": data.get("is_subscribed"),
            "region_id": data.get("region_id"),
            "district_id": data.get("district_id"),
            "institution_id": data.get("institution_id"),
            "grade": data.get("grade"),
        })

    def signup(self, olympiad_id: int) -> dict:
        return self.api.put("olympiad/sign-up", {
            "student_id": self.id,
            "olympiad_id": olympiad_id
        })


def student_decorator(func):
    @wraps(func)
    def _decorator(update, context):
        return func(update, context, student=context.user_data.get('student'))
    return _decorator
