
import pytest
import allure
from playwright.sync_api import Page
from models.page_register_models import CinescopRegisterPage
from utils.datagenerator import DataGenerator

@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
@pytest.mark.smoke
class TestRegisterPage:

    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self, page: Page):

        random_email = DataGenerator.generate_random_email()
        random_name = DataGenerator.generate_random_name()
        random_password = DataGenerator.generate_random_password()

        register_page = CinescopRegisterPage(page)
        register_page.open()
        register_page.register(f"PlaywrightTest {random_name}", random_email,
                               random_password, random_password)

        register_page.assert_was_redirect_to_login_page()
        register_page.make_screenshot_and_attach_to_allure()
        register_page.assert_allert_was_pop_up()
