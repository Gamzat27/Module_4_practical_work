from constants import LOGIN_ENDPOINT

class AuthAPI:
    def __init__(self, requester):
        self.requester = requester

    def login(self, creds):
        return self.requester.send_request(method="POST", endpoint=LOGIN_ENDPOINT, data=creds)