from constants import LOGIN_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url="https://auth.dev-cinescope.coconutqa.ru")

    def login(self, creds, expected_status=201):
        return self.send_request(method="POST", endpoint=LOGIN_ENDPOINT,
                                 data=creds, expected_status=expected_status)