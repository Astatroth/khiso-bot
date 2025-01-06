import datetime
import logging
import os
from core.AppConfig import AppConfig
from kink import inject
from logging.handlers import TimedRotatingFileHandler
from pprint import pformat


@inject
class Logger:
    def __init__(self, config: AppConfig):
        log_dir = os.path.join(os.path.dirname(__file__), '../storage/logs')
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, '{:%Y-%m-%d}.log'.format(datetime.datetime.now()))

        # Настройка ротации логов
        handler = TimedRotatingFileHandler(
            filename=log_file,
            when="midnight",  # Ротация логов раз в сутки
            interval=1,  # Интервал ротации
            backupCount=7,  # Хранить 7 файлов логов
            encoding="utf-8"
        )

        # Настройка формата
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(handler)

        if config.APP_DEBUG.lower() == "true":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def info(self, msg, extra=None):
        self.logger.info(pformat(msg), extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warning(self, msg, extra=None):
        self.logger.warning(msg, extra=extra)
