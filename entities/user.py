
from clients.api_manager import ApiManager

class User:
    """
    Представляет пользователя приложения.

    Attributes:
        email (str): Email пользователя.
        password (str): Пароль пользователя.
        roles (list): Список ролей пользователя (например, ['USER', 'ADMIN']).
        api (ApiManager): Экземпляр `ApiManager` для взаимодействия с API от имени пользователя.

    Example:
        >>> api = ApiManager(...)
        >>> u = User(email="a@b.com", password="pwd", roles=["USER"], api=api)
        >>> u.email
        'a@b.com'
    """
    def __init__(self, email: str, password: str, roles: list, api: ApiManager):
        super().__init__()
        self.email = email
        self.password = password
        self.roles = roles
        self.api = api

    @property
    def creds(self):
        """
        Возвращает учетные данные пользователя.
        Returns:
        tuple: Кортеж `(email, password)`.
        Example:
            >>> u.creds
            ('a@b.com', 'pwd')
        """
        return self.email, self.password
