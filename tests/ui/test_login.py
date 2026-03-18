
import pytest
import allure
import time
from playwright.sync_api import sync_playwright, Page
from models.page_login_models import CinescopLoginPage


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Логин юзера, который уже есть в базе.")
@pytest.mark.smoke
def test_login_by_ui(registered_user, page: Page):

     with allure.step("Создаем объект страницы регистрации cinescope"):
          login_page = CinescopLoginPage(page)

     with allure.step("Открываем страницу"):
          login_page.open()
          login_page.login(registered_user["email"], registered_user["password"])

     with allure.step("Проверка редиректа на домашнюю страницу"):
          login_page.wait_redirect_to_home_page()

     with allure.step("Проверка появления и исчезновения алерта"):
          login_page.check_allert()

     time.sleep(5)
