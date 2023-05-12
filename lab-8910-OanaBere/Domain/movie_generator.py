import random

from Service.film_service import FilmService


class MovieGenerator:
    def __init__(self, film_service: FilmService):
        self.film_service = film_service
        self.movies = ['Extraction',
                       'Taken',
                       'Allegiant',
                       'Ratatouille',
                       'No time to die',
                       'Fast and furious 7',
                       'Hobbs and Shaw',
                       'Scent of a woman',
                       'The Great Gatsby',
                       'The Benefactor',
                       'The Godfather']

    def generate_movie(self, n: int):
        for i in range(1, n):
            program = ['da', 'nu']
            id_film = str(random.randrange(1, 25))
            titlu = random.choice(self.movies)
            an_aparitie = random.randint(2000, 2020)
            pret_bilet = random.uniform(15, 25)
            pret_bilet = round(pret_bilet, 1)
            in_program = random.choice(program)
            self.film_service.add_film(id_film, titlu, an_aparitie, pret_bilet,
                                       in_program)
