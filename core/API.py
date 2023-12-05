import requests
from core.AppConfig import AppConfig
from core.Logger import Logger
from kink import inject


@inject
class API:
    def __init__(self, config: AppConfig, logger: Logger):
        self.config = config
        self.logger = logger

        self.api_endpoint = self.config.API_PRODUCTION_ENDPOINT \
            if self.config.APP_DEBUG is False else self.config.API_TEST_ENDPOINT
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def get(self, endpoint: str, payload: dict = None):
        _endpoint = endpoint + "?"
        for i in range(len(payload)):
            key = list(payload.keys())[i]
            value = list(payload.values())[i]
            _endpoint += str(key) + "=" + str(value)
            if i < len(payload):
                _endpoint += "&"

        return self.send_request('get', _endpoint, payload)

    def post(self, endpoint: str, payload: dict = None):
        pass

    def send_request(self, method: str, endpoint: str, payload: dict = None):
        request_method = getattr(requests, method)

        response = request_method(
            self.api_endpoint + endpoint,
            headers=self.headers,
            json=payload
        )

        if self.config.APP_DEBUG is True:
            self.logger.info(payload)
            self.logger.info(response.status_code)
            self.logger.info(response.json())

        return response.json()
