import datetime
import logging
import os
from core.AppConfig import AppConfig
from kink import inject


@inject
class Logger:
    def __init__(self, config: AppConfig):
        filename = os.path.dirname(__file__) + '/../storage/logs/{:%Y-%m-%d}.log'.format(datetime.datetime.now())

        logging.basicConfig(
            filename=filename if not config.APP_DEBUG else None,
            level="INFO",
            format='%(asctime)s - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(levelname)s - %(message)s',
            force=True
        )

        self.logger = logging.getLogger()

    def info(self, msg, extra=None):
        self.logger.info(msg, extra=extra)

    def error(self, msg, extra=None):
        self.logger.error(msg, extra=extra)

    def debug(self, msg, extra=None):
        self.logger.debug(msg, extra=extra)

    def warning(self, msg, extra=None):
        self.logger.warning(msg, extra=extra)
