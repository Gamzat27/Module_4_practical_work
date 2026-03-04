
class TestMovieApi:

    def test_create_movie(self, movies_api, created_movie):
        resp = movies_api.create_movie(created_movie, expected_status=201)
        assert resp.json()["name"] == created_movie["name"], ("Имя фильма в тесте не соответствует "
                                                             "имени фильма сгенерированного в фикстуре.")
        assert resp.json()["genreId"] == created_movie["genreId"]
        assert resp.json()["price"] == created_movie["price"], "Цены фильмов не совпадают."

        get_resp = movies_api.get_movie(movie_id=resp.json()["id"], expected_status=200)
        assert get_resp.json()["name"] == resp.json()["name"], "Имена не сходятся."

    def test_delete_movie(self, movies_api, my_get_film):
        movies_api.delete_movie(movie_id=my_get_film["id"], expected_status=200)
        movies_api.get_movie(movie_id=my_get_film["id"], expected_status=404)


    def test_get_movie(self, movies_api, my_get_film):
        movie_id = my_get_film["id"]
        resp = movies_api.get_movie(movie_id=movie_id, expected_status=200)
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


    # негативные кейсы
    def test_create_movie_unauthorized(self, unauthenticated_movies_api, created_movie):
        unauthenticated_movies_api.create_movie(created_movie, expected_status=401)

    def test_delete_movie_not_found(self, movies_api):
        movies_api.delete_movie(movie_id=9999999, expected_status=404)

    def test_get_movie_not_found(self, movies_api):
        movies_api.get_movie(movie_id=9999999, expected_status=404)

    def test_get_movies_bad_params(self, movies_api):
        movies_api.get_movies(params={"pageSize": -5}, expected_status=400)

    def test_update_unauthorized(self, unauthenticated_movies_api, my_get_film, created_movie):
        unauthenticated_movies_api.update_movie(movie_id=my_get_film["id"], data=created_movie,
                                                       expected_status=401)

