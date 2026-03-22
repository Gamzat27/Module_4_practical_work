
import allure
import pytest
from models.pydantic_models import RegisterUserResponse

class TestUser:

    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, super_admin, creation_user_data):
        response = super_admin.api.user_api.create_user(creation_user_data, expected_status=201).json()
        created_user_response = RegisterUserResponse(**response)
        assert created_user_response.email == creation_user_data.email, "Email не совпадает"
        assert created_user_response.email == creation_user_data.email, "Email не совпадает"
        assert created_user_response.id, "ID должен быть не пустым"
        assert created_user_response.fullName == creation_user_data.fullName
        assert created_user_response.roles == creation_user_data.roles
        assert created_user_response.verified is True

    @allure.severity(allure.severity_level.CRITICAL)
    def test_get_user_by_locator(self, super_admin, creation_user_data):
        created_user_response = super_admin.api.user_api.create_user(creation_user_data, expected_status=201).json()
        created_user_response = RegisterUserResponse(**created_user_response)
        assert created_user_response.id is not None, "Поле id не должно быть пустым."
        assert created_user_response.email == creation_user_data.email, "email должны быть равны."
        assert created_user_response.roles == creation_user_data.roles, "Роли должны совпадать."
        assert created_user_response.fullName == creation_user_data.fullName, "Имя должно совпадать."

    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.slow
    def test_get_user_by_id_common_user(self, common_user):
        common_user.api.user_api.get_user_info(common_user.email, expected_status=403)

    @allure.severity(allure.severity_level.CRITICAL)
    def test_db_requests(self, super_admin, db_helper, created_test_user):
        assert created_test_user == db_helper.get_user_by_id(created_test_user.id)
        assert db_helper.user_exists_by_email("api1@gmail.com")
