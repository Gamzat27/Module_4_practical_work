from constants import MOVIES_ENDPOINT

class MoviesAPI:
    def __init__(self, requester):
        self.requester = requester

    def create(self, data, expected_status=201):
        return self.requester.send_request("POST", MOVIES_ENDPOINT, data=data, expected_status=expected_status)