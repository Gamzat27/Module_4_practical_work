
import time
import pytest
import allure
from models.page_register_models import CinescopRegisterPage
from utils.datagenerator import DataGenerator

@pytest.mark.smoke
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Регистрация нового пользователя.")
def test_register_by_ui(page) -> None:
    with allure.step(f"Создание юзера для регистрации."):
        random_email: str = DataGenerator.generate_random_email()
        random_name: str = DataGenerator.generate_random_name()
        random_password: str = DataGenerator.generate_random_password()

    with allure.step("Создания объекта класса CinescopRegisterPage c использованием фикстуры page."):
        register_page = CinescopRegisterPage(page)

    with allure.step("Процесс открытия страницы /register, заполнения полей и клик по кнопке 'Зарегестрироваться'."):
        register_page.open()
        register_page.register(full_name=f"PlaywrightTest {random_name}", email=random_email,
                           password=random_password, confirm_password=random_password)
    with allure.step("Убеждаемся, что перенаправление на эдпоинт '/login' прошло и аллерт вышел."):
        register_page.wait_redirect_to_login_page()
        register_page.check_allert()

    time.sleep(5)
