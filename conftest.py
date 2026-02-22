
import pytest
import requests
from tests.api.api_manager import ApiManager
from utils.datagenerator import DataGenerator
from custom_requester.custom_requester import CustomRequester
from constants import ADMIN_CRED

@pytest.fixture(scope="function")
def my_test_film(admin_api):
    data = DataGenerator.generate_movie()
    return data

@pytest.fixture(scope="function")
def my_get_film(admin_api):
    payload = DataGenerator.generate_movie()
    create_resp = admin_api.movies.create_movie(payload, expected_status=201)
    movie = create_resp.json()
    yield movie

@pytest.fixture(scope="function")
def get_movie(admin_api):
    payload = DataGenerator.generate_movie()
    create_resp = admin_api.movies.create_movie(payload, expected_status=201)
    movie = create_resp.json()
    yield movie

@pytest.fixture(scope="session")
def session():
    s = requests.Session()
    yield s
    s.close()

@pytest.fixture(scope="session")
def requester(session):
    # base_url можно указывать None и в API формировать полный URL, либо создать два requester'а
    r = CustomRequester(session=session, base_url=None)
    yield r

@pytest.fixture(scope="session")
def api_manager(session):
    # ApiManager должен принимать requester (см. ниже). Можно также создать два requester's внутри ApiManager.
    return ApiManager(session=session)

@pytest.fixture(scope="session")
def admin_api(api_manager, session):
    # логин через AuthAPI; кладём токен (если есть) в session.headers
    resp = api_manager.auth.login(ADMIN_CRED)
    resp.raise_for_status()
    try:
        token = resp.json().get("accessToken")
    except Exception:
        token = None
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})
    # если сервер установил cookie — requests.Session их уже сохранил
    return api_manager

@pytest.fixture(scope="session")
def movies_api(admin_api):
    # просто возвращаем manager.movies — он использует ту же session
    return admin_api.movies