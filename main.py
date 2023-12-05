from core.Application import Application
from core.AppConfig import AppConfig
from core.Logger import Logger
from core.TranslationManager import TranslationManager
from kink import di


di[AppConfig] = AppConfig()
di[Logger] = Logger()
di[TranslationManager] = TranslationManager()


def main() -> None:
    Application().run()


if __name__ == '__main__':
    main()
