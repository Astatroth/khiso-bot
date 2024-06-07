from core.API import API
from kink import inject


@inject
class Sms:
    def __init__(self, api: API):
        self.api = api

    def send_code(self, phone_number: str, language: str):
        self.api.append_headers({'Accept-Language': language})
        self.api.post("code/send", {
            "phone_number": phone_number
        })

    def validate_code(self,  phone_number: str, code: str, language: str) -> dict:
        self.api.append_headers({'Accept-Language': language})

        return self.api.post("code/verify", {
            "phone_number": phone_number,
            "code": code
        })
