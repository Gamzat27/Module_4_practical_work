

class TestAuthAPI:

    def test_register_user(self, api_manager, add_test_user):
        response = api_manager.auth_api.register_user(add_test_user)
        response_data = response.json()
        assert response_data["email"] == add_test_user["email"], "Email не совпадает"
        assert "id" in response_data, "ID пользователя отсутствует в ответе"
        assert "roles" in response_data, "Роли пользователя отсутствуют в ответе"
        assert "USER" in response_data["roles"], "Роль USER должна быть у пользователя"

    def test_register_and_login_user(self, api_manager, registered_user):
        response = api_manager.auth_api.login_user(registered_user)
        response_data = response.json()
        assert "accessToken" in response_data, "Токен доступа отсутствует в ответе"
        assert response_data["user"]["email"] == registered_user["email"], "Email не совпадает"
