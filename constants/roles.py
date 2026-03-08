
from enum import Enum

class Roles(str, Enum):
    """
    Перечисление ролей пользователей в приложении.

    Значения:
      - USER: обычный пользователь.
      - ADMIN: пользователь с правами администратора.
      - SUPER_ADMIN: супер‑администратор с расширенными правами.

    Пример использования:
        >>> Roles.USER
        <Roles.USER: 'USER'>
        >>> Roles.USER.value
        'USER'
    """
    USER = "USER"
    ADMIN = "ADMIN"
    SUPER_ADMIN = "SUPER_ADMIN"