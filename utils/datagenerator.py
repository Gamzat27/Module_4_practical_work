
import random
from faker import Faker

faker = Faker(locale="ru_RU")

class DataGenerator:
    LOCATIONS = ["SPB", "MSK"]
    GENRE_IDS = list(range(1, 11))
    IMAGE_URLS = [
        "https://img.freepik.com/free-photo/nature-landscape-with-starry-clear-sky_23-2151683130.jpg?semt=ais_hybrid&w=740&q=80",
        "https://img.freepik.com/premium-photo/galaxy-wallpaper_1134901-199264.jpg?semt=ais_hybrid&w=740",
        "https://cdnb.artstation.com/p/assets/images/images/089/846/525/large/chrissectest2-sub-zero-scorpion-5120x2880-17601.jpg?1752102644",
        "https://i.pinimg.com/736x/a4/f9/0a/a4f90af343749c64e6bd551af78e8408.jpg",
        "https://avatars.mds.yandex.net/i?id=6de842b43efc2b17d6bc840a003ccb71_l-3788438-images-thumbs&n=13",
    ]

    @staticmethod
    def random_price(min_price=50, max_price=500):
        return random.randint(min_price, max_price)

    @classmethod
    def random_image_url(cls):
        return random.choice(cls.IMAGE_URLS)

    @classmethod
    def generate_movie(cls):
        return {
            "name": faker.sentence(nb_words=3).rstrip("."),
            "imageUrl": cls.random_image_url(),
            "price": cls.random_price(),
            "description": faker.paragraph(nb_sentences=2),
            "location": random.choice(cls.LOCATIONS),
            "published": faker.boolean(chance_of_getting_true=75),
            "genreId": random.choice(cls.GENRE_IDS),
        }

    @classmethod
    def generate_user(cls, email=None, full_name=None, password=None):
        # по умолчанию генерируем данные, если не переданы
        if email is None:
            email = faker.unique.email()
        if full_name is None:
            full_name = faker.name()
        if password is None:
            # faker.password позволяет задать требования: длину и наличие цифр/символов/регистра
            password = faker.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)

        return {
            "email": email,
            "fullName": full_name,
            "password": password,
            "passwordRepeat": password
        }

    @classmethod
    def generate_random_email(cls):
        return faker.unique.email()
    @classmethod
    def generate_random_password(cls):
        return faker.password(length=10, special_chars=False, digits=True, upper_case=True, lower_case=True)
    @classmethod
    def generate_random_name(cls):
        return faker.name()
