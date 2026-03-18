
from playwright.sync_api import Page

class CinescopLoginPage:

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.url: str = "https://dev-cinescope.coconutqa.ru/login"

        # Локаторы элементов
        self.home_button: str = "a[href='/' and text()='Cinescope']"
        self.all_movies_button: str = "a[href='/movies' and text()='Все фильмы']"

        self.email_input: str = "input[name='email']"
        self.password_input: str = "input[name='password']"

        self.login_button = page.locator('button[type="submit"]:has-text("Войти")')
        self.register_button: str = "a[href='/register' and text()='Зарегистрироваться']"

    # Обработчики локаторов на шапке страницы
    def go_to_home_page(self) -> None:
        """Переход на главную страницу"""
        self.page.click(self.home_button)
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")  # Ожидание загрузки главной страницы

    def go_to_all_movies(self) -> None:
        """Переход на страницу 'Все фильмы'"""
        self.page.click(self.all_movies_button)
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/movies")  # Ожидание загрузки страницы

    # Обработчики локаторов на теле страницы
    def open(self) -> None:
        """Переход на страницу входа"""
        self.page.goto(self.url)

    def enter_email(self, email: str) -> None:
        """Ввод email"""
        self.page.fill(self.email_input, email)

    def enter_password(self, password: str) -> None:
        """Ввод пароля"""
        self.page.fill(self.password_input, password)

    def click_login_button(self) -> None:
        """Клик по кнопке входа"""
        self.login_button.click()

    # Вспомогательные action методы
    def login(self, email: str, password: str) -> None:
        """Полный процесс входа"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()

    def wait_redirect_to_home_page(self) -> None:
        """Ожидание перехода на домашнюю страницу"""
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")  # Ожидание загрузки домашней страницы
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/", "Редирект на домашнюю старницу не произошел"

    def check_allert(self) -> None:
        """Проверка всплывающего сообщения после редиректа"""
        # Проверка появления алерта с текстом "Вы вошли в аккаунт"
        notification_locator = self.page.get_by_text("Вы вошли в аккаунт")
        notification_locator.wait_for(state="visible")  # Ждем появления элемента
        assert notification_locator.is_visible(), "Уведомление не появилось"

        # Ожидание исчезновения алерта
        notification_locator.wait_for(state="hidden")  # Ждем, пока алерт исчезнет
        assert notification_locator.is_visible() == False, "Уведомление исчезло"