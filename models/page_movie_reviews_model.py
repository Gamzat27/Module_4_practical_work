
from models.base_page_model import BasePage
from playwright.sync_api import Page

class PageMovieReviews(BasePage):

    def __init__(self, login_page: Page) -> None:
        super().__init__(page=login_page)
        self.movie_url = f"{self.home_url}movies/"

        self.movies_all = 'a[href="/movies"]:has-text("Все фильмы")'
        self.input_placeholder = 'textarea[placeholder="Написать отзыв"]'
        self.rating_button = 'button[role="combobox"]'
        self.send_button = 'button[type="submit"]:has-text("Отправить")'

    def reviews_movie(self, input_text, movie_id):
        if not self.page.url.endswith("/movies"):
            self.click_element(self.movies_all)
        self.open_url(f"{self.movie_url}{movie_id}")
        self.enter_text_to_element(locator=self.input_placeholder, text=input_text)
        self.click_element(self.rating_button)
        self.page.get_by_role("option", name="4").click()
        self.click_element(self.send_button)

    # Проверки
    def is_review_posted(self, input_text, timeout: int = 5000) -> bool:
        review_locator = f'text="{input_text}"'
        try:
            self.page.wait_for_selector(review_locator, timeout=timeout)
            return True
        except Exception:
            return False

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Отзыв успешно создан")