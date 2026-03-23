import pytest
import allure
from conftest import common_user, admin_user
from models.pydantic_models import MovieSchema

@allure.epic("Тестирование эндпоинта '/movies'.")
@allure.story("Тестирование создания, получения, изменения и удаления фильмов.")
class TestMovieApi:

    @allure.feature("Тестирование создания фильма")
    @allure.label("qa_name", "Gamzat")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.step("Запуск теста на создание фильма")
    @pytest.mark.smoke
    def test_create_movie(self, movies_api, created_movie, db_helper):
        with allure.step(f"Отправка post запроса на создание фильма c name: {created_movie['name']}"):
            resp = movies_api.create_movie(created_movie, expected_status=201)
            movie = MovieSchema(**resp.json())
            assert movie.name == created_movie["name"], ("Имя фильма в тесте не соответствует "
                                                             "имени фильма сгенерированного в фикстуре.")
            assert movie.genreId == created_movie["genreId"]
            assert movie.price == created_movie["price"], "Цены фильмов не совпадают."
            assert db_helper.movie_exists_by_name(name=resp.json()["name"]) == True

        with allure.step(f"Отправка get запроса на получение созданного фильма по id: {resp.json()['id']}"):
            get_resp = movies_api.get_movie(movie_id=resp.json()["id"], expected_status=200)
            assert get_resp.json()["name"] == resp.json()["name"], "Имена не сходятся."
            movie = db_helper.get_movie_by_name(name=resp.json()["name"])
            assert movie.name == created_movie["name"], "Названия в бд отличается."


    @allure.feature("Удаление фильма.")
    @allure.step("Запуск теста на удаление фильма по id.")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("Qa_name", "Gamzat")
    @pytest.mark.smoke
    @pytest.mark.parametrize(
        "user, expected_delete_status",
        [
            pytest.param("common_user", 403, marks=pytest.mark.slow, id="slow-case-common_user"),
            pytest.param("admin_user", 200, marks=pytest.mark.slow, id="slow-case-admin_user"),
            ("super_admin", 200),
        ],
        indirect=["user"]
    )
    def test_delete_movie(self, user, movies_api, my_get_film, expected_delete_status):
        with allure.step(f"Запуск попытка удалить фильм с ролью: {user}"):
            user.api.movies_api.delete_movie(movie_id=my_get_film["id"], expected_status=expected_delete_status)

            if expected_delete_status == 200:
                user.api.movies_api.get_movie(movie_id=my_get_film["id"], expected_status=404)
            else:
                user.api.movies_api.get_movie(movie_id=my_get_film["id"], expected_status=200)


    @pytest.mark.flaky(reruns=3, rerans_delay=5)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("Qa_name", "Gamzat")
    @allure.feature("Получение фильма.")
    @allure.step("Запуск теста на получение фильма.")
    @pytest.mark.smoke
    def test_get_movie(self, movies_api, my_get_film, db_helper):
        movie_id = my_get_film["id"]
        name = my_get_film["name"]
        resp = movies_api.get_movie(movie_id=movie_id, expected_status=200)
        assert resp.json()["id"] == movie_id, "id не совпадают."
        movie = db_helper.get_movie_by_name(name=resp.json()["name"])
        assert movie is not None, "В базе нет запись с таким именем."
        assert movie.name == name, "Название фильма не совпадает с тем, что в базе."
        assert db_helper.movie_exists_by_name(name=name) == True, "Фильма с таким названием в базе не существует."


    def test_get_movies(self, movies_api):
        resp = movies_api.get_movies(expected_status=200)
        body = resp.json()
        assert "movies" or "data" in body, "В ответе нет ключа 'movies'."
        assert "count" in body, "В теле не указанно кол-во фильмов на сайте."
        assert "page" in body
        assert  "pageSize" in body
        assert "pageCount" in body


    def test_get_movies_params(self, movies_api):
        resp = movies_api.get_movies(params={"locations": "MSK"}, expected_status=200)
        movies = resp.json()["movies"]
        assert any(m["location"] == "MSK" for m in movies), "В выборку попали фильмы не только из Москвы."


    def test_update_movie(self, movies_api, my_get_film, created_movie):
        new_data = created_movie
        resp = movies_api.update_movie(movie_id=my_get_film["id"], data=new_data, expected_status=200)
        assert resp.json()["name"] == new_data["name"]

        movies_api.get_movie(movie_id=resp.json()["id"], expected_status=200)
        assert resp.json()["name"] == new_data["name"], "Имена не совпадают с изменениями."

    @allure.description("Поиск фильмов по локации")
    @pytest.mark.parametrize("locations", ["MSK", "SPB"])
    def test_get_movies_parametrize(self, movies_api, locations):
        response = movies_api.get_movies(params={"locations": locations}, expected_status=200)
        movies = response.json()["movies"]
        for movie in movies:
            assert movie["location"] == locations


    # негативно-позитивный кейсы
    @allure.description("Попытка добавить фильм с ролью 'user'.")
    @pytest.mark.slow
    def test_create_movie_with_user_rights(self, movies_api, common_user, created_movie):
        response = common_user.api.movies_api.create_movie(data=created_movie, expected_status=403)
        assert response.json()["message"] == "Forbidden resource"
        assert response.json()["error"] == "Forbidden"

    @allure.description("Попытка добавить фильм с ролью 'admin'")
    @pytest.mark.slow
    def test_create_movie_with_admin_rights(self, movies_api, admin_user, created_movie):
        response = admin_user.api.movies_api.create_movie(data=created_movie, expected_status=201)
        assert response.json()["name"] == created_movie["name"]

    # негативные кейсы
    @allure.description("Попытка добавить фильм не авторизованным.")
    def test_create_movie_unauthorized(self, unauthenticated_movies_api, created_movie):
        unauthenticated_movies_api.create_movie(created_movie, expected_status=401)

    @allure.description("Попытка удалить несуществующий фильм.")
    def test_delete_movie_not_found(self, movies_api):
        movies_api.delete_movie(movie_id=9999999, expected_status=404)

    @allure.description("Попытка получить несуществующий фильм.")
    def test_get_movie_not_found(self, movies_api):
        movies_api.get_movie(movie_id=9999999, expected_status=404)

    @allure.description("Попытка получить фильм с неверными параметрами.")
    def test_get_movies_bad_params(self, movies_api):
        movies_api.get_movies(params={"pageSize": -5}, expected_status=400)

    @allure.description("Попытка удалить фильм не авторизованным.")
    @pytest.mark.regression
    def test_update_unauthorized(self, unauthenticated_movies_api, my_get_film, created_movie):
        unauthenticated_movies_api.update_movie(movie_id=my_get_film["id"], data=created_movie,
                                                       expected_status=401)
