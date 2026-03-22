import pytest
import allure
from models.pydantic_models import RegisterUserResponse
from clients.api_manager import ApiManager


class TestAuthAPI:

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_register_user(self, api_manager: ApiManager, creation_user_data):
        response = api_manager.auth_api.register_user(user_data=creation_user_data)
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == creation_user_data.email, "Email не совпадает"

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_register_and_login_user(self, api_manager, registered_user):
        response = api_manager.auth_api.login_user(login_data=registered_user)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"]
