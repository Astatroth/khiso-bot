import json
from dotenv import load_dotenv, dotenv_values
from os import environ


class AppConfig:

    def __init__(self):
        load_dotenv()

        [setattr(self, key, value) for key, value in dotenv_values('.env').items()]

    def __getattr__(self, item):
        attr = environ.get(item.upper())

        return attr
