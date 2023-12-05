from core.Logger import Logger
from kink import inject


@inject
class BaseHandler:

    def __init__(self, end: int, logger: Logger):
        self.end = end
        self.logger = logger
