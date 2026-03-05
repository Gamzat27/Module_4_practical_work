

from clients.api_manager import ApiManager

class User:
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api  # Сюда будем передавать экземпляр API Manager для запросов

    @property
    def creds(self): # Декоратор @property делает метод creds доступным как атрибут - email, password = user.creds
        """Возвращает кортеж (email, password)"""
        return self.email, self.password