from core.API import API
from core.Logger import Logger
from kink import inject
from typing import List


@inject
class Subscription:
    def __init__(self, api: API, logger: Logger):
        self.api = api
        self.logger = logger

    def get_subscriptions(self) -> List:
        response = self.api.get("channels")

        return response.get("channels")

