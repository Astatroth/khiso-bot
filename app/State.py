from enum import Enum


class State(Enum):
    SET_LANGUAGE: int = 1
    AWAIT_SUBSCRIPTION: int = 3
    AWAIT_CONTACT: int = 4
    AWAIT_NAME: int = 5
    AWAIT_GENDER: int = 7
    AWAIT_DATE_OF_BIRTH: int = 8
    AWAIT_REGION: int = 9
    AWAIT_DISTRICT: int = 10
    AWAIT_INSTITUTION: int = 11
    AWAIT_GRADE: int = 12
    VALIDATE_CODE: int = 13
    AWAIT_ANSWER: int = 50
    IDLE: int = 1000
