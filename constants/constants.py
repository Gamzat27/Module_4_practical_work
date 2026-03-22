
BASE_URL_MOVIES = "https://api.dev-cinescope.coconutqa.ru" # базовый url для фильмов
MOVIES_ENDPOINT = "/movies/" # фильмы
GENRES_ENDPOINT = "/genres" # жанры

BASE_URL_AUTH = "https://auth.dev-cinescope.coconutqa.ru" # авторизация базовый url
LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"

# Заголовки для запросов
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Креды админа (имеет все роли)
ADMIN_CRED = {
    "email": "api1@gmail.com",
    "password": "asdqwe123Q"
}

# логин и пароль для супер админа
SUPER_ADMIN_USERNAME = "api1@gmail.com"
SUPER_ADMIN_PASSWORD = "asdqwe123Q"


GREEN = '\033[32m'
RED = '\033[31m'
RESET = '\033[0m'
