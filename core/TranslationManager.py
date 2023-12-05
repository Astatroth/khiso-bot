import i18n
import os
from core.AppConfig import AppConfig
from kink import inject

@inject
class TranslationManager:
    def __init__(self, config: AppConfig):
        i18n.load_path.append(os.path.dirname(os.path.abspath(__file__)) + '/../lang/')
        i18n.set('file_format', 'json')
        i18n.set('skip_locale_root_data', True)
        i18n.set('locale', config.APP_LOCALE)
        i18n.set('fallback', config.APP_FALLBACK_LOCALE)

    def t(self, key: str) -> str:
        return i18n.t(key)
