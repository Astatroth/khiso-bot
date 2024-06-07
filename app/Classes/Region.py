from core.API import API
from core.Logger import Logger
from core.Paginator import Paginator
from core.TranslationManager import TranslationManager
from kink import inject
from typing import Dict


@inject
class Region(Paginator):
    def __init__(self, api: API, i18n: TranslationManager, logger: Logger):
        self.api = api
        self.i18n = i18n
        self.logger = logger

    def format_callback_data(self, item: Dict) -> str:
        return "region_{}".format(item.get('id'))

    def get_regions(self, limit: int, page: int = 1):
        response = self.api.get("regions", {
            "page": page,
            "limit": limit
        })

        return self.paginate(response.get("regions")["rows"], response.get("regions")["total"], limit, page)

