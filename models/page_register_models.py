
from playwright.sync_api import Page

class CinescopRegisterPage:

    def __init__(self, page: Page) -> None:
        self.page: Page = page
        self.url: str = "https://dev-cinescope.coconutqa.ru/register"

        # Локаторы элементов
        self.home_button: str = "a[href='/' and text()='Cinescope']"
        self.all_movies_button: str = "a[href='/' and text()='Все фильмы']"

        self.full_name_input = page.locator("input[name='fullName']")
        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.repeat_password_input = page.locator("input[name='passwordRepeat']")
        self.register_button = page.locator('button:has-text("Зарегистрироваться")')
        self.sign_button = page.locator("a:has-text('Войти')")

    # Шапка страницы
    def go_to_home_page(self) -> None:
        """Переход на главную страницу."""
        self.page.click(selector=self.all_movies_button)
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/") # ждет, пока страница загрузится

    def go_to_all_movies(self) -> None:
        """Переход на страницу 'Все фильмы'."""
        self.page.click(selector=self.all_movies_button)
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/movies") # метод wait_for_url ждет
        # пока страница загрузится

    # Тело страницы
    def open(self) -> None:
        """Переход на страницу регистрации."""
        self.page.goto(self.url)

    def enter_full_name(self, full_name: str) -> None:
        """Ввод full_name"""
        self.full_name_input.fill(full_name)

    def enter_email(self, email: str) -> None:
        """Вод email."""
        self.email_input.fill(email)

    def enter_password(self, password: str) -> None:
        """Ввод password."""
        self.password_input.fill(password)

    def enter_repeat_password(self, repeat_password: str) -> None:
        """Ввод подтверждения пароля"""
        self.repeat_password_input.fill(repeat_password)

    def click_register_button(self) -> None:
        """Клик по кнопке регистрации"""
        from playwright.sync_api import expect
        expect(self.register_button).to_be_enabled(timeout=7000)
        self.register_button.click()

    # Вспомогательные action методы
    def register(self, full_name: str, email: str, password: str, confirm_password: str) -> None:
        """Полный процесс регистрации."""
        self.enter_full_name(full_name)
        self.enter_email(email)
        self.enter_password(password)
        self.enter_repeat_password(confirm_password)
        self.click_register_button()

    def wait_redirect_to_login_page(self):
        """Переход на страницу login."""
        self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/login")  # Ожидание загрузки страницы login
        assert self.page.url == "https://dev-cinescope.coconutqa.ru/login", "Редирект на домашнюю старницу не произошел"

    def check_allert(self):
        """Проверка всплывающего сообщения после редиректа"""
        # Проверка появления алерта с текстом "Подтвердите свою почту"
        notification_locator = self.page.get_by_text("Подтвердите свою почту")
        notification_locator.wait_for(state="visible")  # Ждем появления элемента

        assert notification_locator.is_visible(), "Уведомление не появилось"
        # Ожидание исчезновения алерта
        notification_locator.wait_for(state="hidden")  # Ждем, пока алерт исчезнет
        assert notification_locator.is_visible() == False, "Уведомление исчезло"
