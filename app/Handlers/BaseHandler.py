from core.Logger import Logger
from core.TranslationManager import TranslationManager
from kink import inject


@inject
class BaseHandler:

    def __init__(self, end: int, i18n: TranslationManager, logger: Logger):
        self.end = end
        self.logger = logger
        self.i18n = i18n
