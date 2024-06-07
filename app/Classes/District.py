from core.API import API
from core.Logger import Logger
from core.Paginator import Paginator
from core.TranslationManager import TranslationManager
from kink import inject
from typing import Dict


@inject
class District(Paginator):
    def __init__(self, api: API, i18n: TranslationManager, logger: Logger):
        self.api = api
        self.i18n = i18n
        self.logger = logger

    def format_callback_data(self, item: Dict) -> str:
        return "district_{}".format(item.get('id'))

    def get_districts(self, region_id: int, limit: int, page: int = 1):
        response = self.api.get("districts", {
            "region_id": region_id,
            "page": page,
            "limit": limit
        })

        return self.paginate(
            response.get("districts")["rows"],
            response.get("districts")["total"],
            limit,
            page,
            display_back_button=True
        )
