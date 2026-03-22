
import pytest
import allure
from playwright.sync_api import Page
from models.page_login_models import CinescopLoginPage


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
@pytest.mark.smoke
class TestloginPage:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, registered_user, page: Page):

        login_page = CinescopLoginPage(page)
        login_page.open()
        login_page.login(registered_user["email"], registered_user["password"])

        login_page.assert_was_redirect_to_home_page()
        login_page.make_screenshot_and_attach_to_allure()
        login_page.assert_allert_was_pop_up()
