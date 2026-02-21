
class TestMovieApi:

    def test_create_movie(self, movies_api, my_test_film):
        resp = movies_api.create(my_test_film, expected_status=201)
        assert resp.status_code == 201, "Статус код не соответствует ожидаемому."
        assert resp.json()["name"] == my_test_film["name"], ("Имя фильма в тесте не соответствует "
                                                             "имени фильма сгенерированного в фикстуре.")


