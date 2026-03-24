import allure
from playwright.sync_api import Page

class PageAction:

    def __init__(self, page: Page) -> None:
        self.page: Page = page

    def open_url(self, url: str) -> None:
        with allure.step(f"Переход на страницу: {url}"):
            self.page.goto(url)

    def enter_text_to_element(self, locator: str, text: str) -> None:
        with allure.step(f"Ввод текста '{text}' в поле '{locator}'"):
            self.page.fill(locator, text)

    def click_element(self, locator: str) -> None:
        with allure.step(f"Клик по элементу '{locator}'"):
            self.page.click(locator)

    def wait_redirect_for_url(self, url: str) -> None:
        with allure.step(f"Ожидание загрузки страницы {url}"):
            self.page.wait_for_url(url)
            assert self.page.url == url, "Редирект на домашнюю страницу не произошел."

    def get_element_txt(self, locator: str) -> str:
        with allure.step(f"Получение текста элемента: {locator}"):
            return self.page.locator(locator).text_content()

    def wait_for_element(self, locator: str, state: str = "visible") -> None:
        with allure.step(f"Ожидание элемента '{locator}', state = {state}"):
            self.page.locator(locator).wait_for(state=state)

    def make_screenshot_and_attach_to_allure(self) -> None:
        with allure.step("Скриншот текущей страницы"):
            screenshot_path = "screenshots.png"
            self.page.screenshot(path=screenshot_path, full_page=True)
            with open(screenshot_path, mode="rb") as file:
                allure.attach(file.read(), name="Screenshot", attachment_type=allure.attachment_type.PNG)

    def check_pop_up_element_with_text(self, text: str) -> None:
        with allure.step(f"Проверка всплывающего сообщения c текстом: {text}"):
            notification_locator = self.page.get_by_text(text)
            with allure.step(f"Проверка появления алерта с текстом: {text}"):
                notification_locator.wait_for(state="visible")
                assert notification_locator.is_visible(), "Уведомление не появилось"
            with allure.step(f"Проверка исчезновения алерта с текстом: {text}"):
                notification_locator.wait_for(state="hidden")
                assert not notification_locator.is_visible(), "Уведомление не исчезло"
