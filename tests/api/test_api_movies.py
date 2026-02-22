
class TestMovieApi:

    def test_create_movie(self, movies_api, my_test_film):
        resp = movies_api.create_movie(my_test_film, expected_status=201)
        self.movie_id = resp.json()["id"]
        assert resp.status_code == 201, "Статус код не соответствует ожидаемому."
        assert resp.json()["name"] == my_test_film["name"], ("Имя фильма в тесте не соответствует "
                                                             "имени фильма сгенерированного в фикстуре.")
        assert resp.json()["genreId"] == my_test_film["genreId"]
        assert resp.json()["price"] == my_test_film["price"], "Цены фильмов не совпадают."

    def test_delete_movie(self, movies_api, my_get_film):
        resp = movies_api.delete_movie(movie_id=my_get_film["id"], expected_status=200)
        assert resp.status_code == 200, "Не удалось удалить фильм."

    def test_getting_movie(self, movies_api, my_get_film):
        movie_id = my_get_film["id"]
        resp = movies_api.getting_movie(my_get_film=movie_id, expected_status=200)
        assert resp.status_code == 200, "Не удалось получить фильм по Айди."
        assert resp.json()["id"] == movie_id, "Айди фильмов не совпадают."
        assert resp.json()["name"] == my_get_film["name"], "Имена фильмов не совпадают."
        assert resp.json()["price"] == my_get_film["price"], "Цены фильмов не совпадают."
        assert resp.json()["description"] == my_get_film["description"], "Описание фильмов не совпадают."
        assert resp.json()["imageUrl"] == my_get_film["imageUrl"], "Картинки фильмов не совпадают."
        assert resp.json()["location"] == my_get_film["location"]
        assert resp.json()["published"] == my_get_film["published"]
        assert resp.json()["rating"] == my_get_film["rating"]
        assert resp.json()["genreId"] == my_get_film["genreId"]
        assert resp.json()["createdAt"] == my_get_film["createdAt"]
        assert resp.json()["reviews"] is not None
        assert resp.json()["genre"]["name"] == my_get_film["genre"]["name"]

    def test_get_movie_posters(self, movies_api):
        resp = movies_api.get_movie_posters()
        assert resp.status_code == 200, "Не удалось получить афиши к фильмам."

    def test_film_editing(self, movies_api, get_movie, my_test_film):
        new_data = my_test_film
        resp = movies_api.film_editing(movie_id=get_movie["id"], new_data=new_data, expected_status=200)
        assert resp.status_code == 200
        assert resp.json()["name"] == new_data["name"]

    # негативные кейсы

    def test_create_movie_unauthorized(self, movies_api, my_test_film):
        auth = movies_api.requester.session.headers.pop("Authorization", None)
        try:
            resp = movies_api.create_movie(my_test_film, expected_status=401)
            assert resp.status_code in (401, 403)
        finally:
            if auth:
                movies_api.requester.session.headers["Authorization"] = auth

    def test_delete_movie_not_found(self, movies_api):
        resp = movies_api.delete_movie(movie_id=9999999, expected_status=404)
        assert resp.status_code == 404

    def test_getting_movie_not_found(self, movies_api):
        resp = movies_api.getting_movie(my_get_film=9999999, expected_status=404)
        assert resp.status_code == 404

    def test_get_movie_posters_bad_params(self, movies_api):
        url = movies_api.requester.base_url.rstrip('/') + "/movies/posters?limit=-5"
        resp = movies_api.requester.session.get(url, headers=movies_api.requester.session.headers)
        assert resp.status_code in (400, 500)

    def test_film_editing_unauthorized(self, movies_api, get_movie, my_test_film):
        auth = movies_api.requester.session.headers.pop("Authorization", None)
        try:
            resp = movies_api.film_editing(movie_id=get_movie["id"], new_data=my_test_film, expected_status=401)
            assert resp.status_code in (401, 403)
        finally:
            if auth:
                movies_api.requester.session.headers["Authorization"] = auth
