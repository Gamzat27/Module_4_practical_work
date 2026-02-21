from tests.api.auth_api import AuthAPI
from tests.api.movies_api import MoviesAPI
from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL_AUTH, BASE_URL_MOVIES

class ApiManager:

    def __init__(self, session):
        self.auth_requester = CustomRequester(session=session, base_url=BASE_URL_AUTH)
        self.movies_requester = CustomRequester(session=session, base_url=BASE_URL_MOVIES)
        self.auth = AuthAPI(requester=self.auth_requester)
        self.movies = MoviesAPI(requester=self.movies_requester)


