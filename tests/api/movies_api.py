from constants import MOVIES_ENDPOINT

class MoviesAPI:

    def __init__(self, requester):
        self.requester = requester

    def create_movie(self, data, expected_status=201):
        return self.requester.send_request(method="POST", endpoint=MOVIES_ENDPOINT,
                                           data=data, expected_status=expected_status)

    def getting_movie(self, my_get_film, expected_status):
        return self.requester.send_request(method="GET", endpoint=f"{MOVIES_ENDPOINT}{my_get_film}",
                                           expected_status=expected_status)

    def delete_movie(self, movie_id, expected_status=204):
        response = self.requester.send_request(method="DELETE", endpoint=f"{MOVIES_ENDPOINT}{movie_id}",
                                           expected_status=expected_status)
        return response

    def get_movie_posters(self, expected_status=200):
        return self.requester.send_request(method="GET", endpoint=MOVIES_ENDPOINT, expected_status=expected_status)

    def film_editing(self, new_data, movie_id, expected_status=200):
        return self.requester.send_request(method="PATCH", endpoint=f"{MOVIES_ENDPOINT}{movie_id}",
                                           data=new_data, expected_status=expected_status)