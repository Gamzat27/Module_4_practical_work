
from clients.movies_api import MoviesAPI
from clients.auth_api import AuthAPI
from clients.user_api import UserAPI

class ApiManager:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session=session)
        self.movies_api = MoviesAPI(session=session)
        self.user_api = UserAPI(session=session)

    def close_session(self):
        self.session.close()
