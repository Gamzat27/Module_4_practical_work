
import pytest
import requests
import copy
from clients.api_manager import ApiManager
from utils.datagenerator import DataGenerator
from constants.constants import ADMIN_CRED
from resurses.user_creds import SuperAdminCreds
from entities.user import User
from constants.roles import Roles

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

@pytest.fixture
def add_test_user():
    user_data = DataGenerator.generate_user()
    return {
        "email": user_data["email"],
        "fullName": user_data["fullName"],
        "password": user_data["password"],
        "passwordRepeat": user_data["passwordRepeat"],
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="function")
def creation_user_data(add_test_user):
    updated_data = add_test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def registered_user(api_manager, add_test_user):
    api_manager.auth_api.register_user(add_test_user)
    creds = {"email": add_test_user["email"], "password": add_test_user["password"]}
    yield creds


@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


@pytest.fixture
def admin_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.ADMIN.value],
        new_session)

    resp = super_admin.api.user_api.create_user(user_data=creation_user_data)
    user_id = resp.json().get("id")

    base = super_admin.api.user_api.base_url
    session_obj = super_admin.api.session
    session_obj.patch(f"{base}/user/{user_id}", json={"roles": [Roles.USER.value, Roles.ADMIN.value]})

    creds = [creation_user_data['email'], creation_user_data['password']]
    admin_user.api.auth_api.authenticate(creds)
    return admin_user


@pytest.fixture
def user(request):
    return request.getfixturevalue(request.param)