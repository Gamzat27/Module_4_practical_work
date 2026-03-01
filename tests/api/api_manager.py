
from clients.movies_api import MoviesAPI
from clients.auth_api import AuthAPI

class ApiManager:
    def __init__(self, session):
        self.auth = AuthAPI(session=session)
        self.movies = MoviesAPI(session=session)
