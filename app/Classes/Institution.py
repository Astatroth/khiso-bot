from core.API import API
from core.Logger import Logger
from core.Paginator import Paginator
from core.TranslationManager import TranslationManager
from kink import inject
from typing import Dict


@inject
class Institution(Paginator):
    def __init__(self, api: API, i18n: TranslationManager, logger: Logger):
        self.api = api
        self.i18n = i18n
        self.logger = logger

    def format_callback_data(self, item: Dict) -> str:
        return "institution_{}".format(item.get('id'))

    def get_institutions(self, district_id: int, limit: int, page: int = 1):
        response = self.api.get("institutions", {
            "district_id": district_id,
            "page": page,
            "limit": limit
        })

        return self.paginate(
            response.get("institutions")["rows"],
            response.get("institutions")["total"],
            limit,
            page,
            display_back_button=True
        )
