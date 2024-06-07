from app.Keyboard import Keyboard
from typing import Dict


class Paginator:
    def format_callback_data(self, item: Dict) -> str:
        pass

    def paginate(self, data: Dict, total: int, limit: int, page: int = 1, display_back_button: bool = False):
        keyboard = []
        for i in range(len(data)):
            keyboard.append(
                (
                    data[i].get("name"),
                    self.format_callback_data(data[i])
                )
            )

        if page > 1:
            keyboard.append(
                (
                    "\u2B05 " + self.i18n.t("strings.prev"),
                    "prev_{}".format(str(page))
                )
            )

        if total > (limit * page):
            keyboard.append(
                (
                    "\u27A1 " + self.i18n.t("strings.next"),
                    "next_{}".format(str(page))
                )
            )

        if display_back_button:
            keyboard.append(
                (
                    "\u23EA " + self.i18n.t("strings.back"),
                    "back"
                )
            )

        return keyboard
