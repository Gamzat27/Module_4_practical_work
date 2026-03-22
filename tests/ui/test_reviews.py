
import allure
import pytest
from playwright.sync_api import Page
from models.page_movie_reviews_model import PageMovieReviews

@allure.epic("Тестирование UI")
@allure.feature("Тестирование функциональность оставлять отзывов к фильмам.")
@pytest.mark.ui
@pytest.mark.smoke
class TestReviews:

    @pytest.mark.flaky(reruns=5, reruns_delay=5)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Оставить успешно отзыв к фильму.")
    def test_reviews(self, my_get_film, login_page: Page) -> None:
        movie_id = my_get_film["id"]
        reviews_page = PageMovieReviews(login_page)
        reviews_page.reviews_movie(input_text="Тестовый отзыв к фильму!", movie_id=movie_id)

        reviews_page.is_review_posted(input_text="Тестовый отзыв к фильму!")
        reviews_page.make_screenshot_and_attach_to_allure()
        reviews_page.assert_allert_was_pop_up()
