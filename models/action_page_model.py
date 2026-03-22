
import allure
from playwright.sync_api import Page

class PageAction:

    def __init__(self, page: Page) -> None:
        self.page: Page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str) -> None:
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str) -> None:
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str) -> None:
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы '{url}'")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, "Редирект на домашнюю страницу не произошел."

    @allure.step("Получение текста элемента: {locator}")
    def get_element_txt(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible") -> None:
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей стрaницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshots.png"
        self.page.screenshot(path=screenshot_path, full_page=True) # True - скриншот всей страницы.

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path,  mode="rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect", attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> None:
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            # Ждем появления элемента
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            # Ждем, пока алерт исчезнет
            notification_locator.wait_for(state="hidden")
            assert notification_locator.is_visible() == False, "Уведомление не исчезло"
