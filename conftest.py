
import pytest
import requests
import copy
from clients.api_manager import ApiManager
from utils.datagenerator import DataGenerator
from constants import ADMIN_CRED

@pytest.fixture(scope="function")
def created_movie(admin_api):
    data = DataGenerator.generate_movie()
    return data

@pytest.fixture(scope="function")
def my_get_film(admin_api):
    payload = DataGenerator.generate_movie()
    create_resp = admin_api.movies_api.create_movie(payload, expected_status=201)
    movie = create_resp.json()
    yield movie

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    session = requests.Session()
    yield session
    session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session=session)

@pytest.fixture(scope="session")
def admin_api(api_manager, session):
    resp = api_manager.auth_api.login_user(ADMIN_CRED)
    resp.raise_for_status()
    try:
        token = resp.json().get("accessToken")
    except Exception:
        token = None
    if token:
        session.headers.update({"Authorization": f"Bearer {token}"})
    return api_manager

@pytest.fixture(scope="session")
def movies_api(admin_api):
    return admin_api.movies_api

@pytest.fixture(scope="function")
def unauthenticated_movies_api(movies_api):
    session = requests.Session()
    session.headers.update({
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    movies_api_copy = copy.copy(movies_api)
    if hasattr(movies_api_copy, "session"):
        movies_api_copy.session = session
    elif hasattr(movies_api_copy, "requester") and hasattr(movies_api_copy.requester, "session"):
        movies_api_copy.requester.session = session
    else:
        raise RuntimeError("Не удалось заменить сессию в копии movies_api.")

    return movies_api_copy

@pytest.fixture(scope="function")
def add_test_user():
    user_data = DataGenerator.generate_user()
    return user_data

@pytest.fixture
def registered_user(api_manager, add_test_user):
    api_manager.auth_api.register_user(add_test_user)
    creds = {"email": add_test_user["email"], "password": add_test_user["password"]}
    yield creds
