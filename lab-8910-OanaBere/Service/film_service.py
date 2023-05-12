from typing import List, Optional

from Domain.add_operation import AddOperation
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class FilmService:
    def __init__(self,
                 film_repository: Repository,
                 film_validator: FilmValidator,
                 undo_redo_service: UndoRedoService):
        self.film_repository = film_repository
        self.film_validator = film_validator
        self.undo_redo_service = undo_redo_service

    def add_film(self,
                 id_film: str,
                 titlu: str,
                 an_aparitie: int,
                 pret_bilet: float,
                 in_program: str):
        """
        functia adauga un nou film
        """
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.film_validator.validate(film)
        self.film_repository.create(film)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.film_repository, film)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_film(self,
                    id_film: str,
                    titlu: str,
                    an_aparitie: int,
                    pret_bilet: float,
                    in_program: str):
        """
        functia actualizeaza un film
        """
        film = Film(id_film, titlu, an_aparitie, pret_bilet, in_program)
        self.film_validator.validate(film)
        self.film_repository.update(film)

    def delete_film(self, id_film: str):
        self.film_repository.delete(id_film)

    def show_all_films(self) -> List[Film]:
        return self.film_repository.read()

    def show_film(self, id_film: str) -> Optional[Film]:
        return self.film_repository.read(id_film)

    def cautare_full_text_film(self, film, sir):

        """
        Cauta in orice valoare a cheilor filmului, un sir dat
        :param film: filmul
        :param sir: sirul dat
        :return: - filmul - daca s-a gasit sirul in film
                 - None - daca nu s-a gasit sirul in film
        """
        if sir in film.id_entity:
            return film

        if sir in film.titlu:
            return film

        if sir in str(film.an_aparitie):
            return film

        if sir in str(film.pret_bilet):
            return film

        if sir in film.in_program:
            return film

        return None

    def cautare_full_text_filme(self, filme, sir):

        """
        Creeaza o lista cu toate filmele dintr-o lista data in care se
        gaseste un sir dat
        :param filme: lista de filme data
        :param sir: sirul dat
        :return: lista de filme in care se gaseste sir
        """

        lista = []
        for film in filme:
            if self.cautare_full_text_film(film, sir):
                lista.append(film)

        return lista

    def numar_rezervari(self, film: Film, rezervari):

        """
        Calculeaza cate rezervari sunt pentru un film
        :param film: filmul
        :param rezervari: lista de rezervari
        :return: numarul de rezervari pt filmul respectiv
        """

        nr_rezervari = 0
        for rezervare in rezervari:
            if film.id_entity == rezervare.id_film:
                nr_rezervari += 1
        return nr_rezervari

    def ordonare_dupa_nr_rezervari(self, filme, rezervari):

        """
        Ordoneaza descrescator o lista de filme dupa numarul de rezervari
        la fiecare film
        :param filme: lista de filme
        :param rezervari: lista de rezervari
        :return: lista ordonata
        """

        for i in range(len(filme) - 1):
            for j in range(i + 1, len(filme)):
                if self.numar_rezervari(filme[i], rezervari) < \
                        self.numar_rezervari(filme[j], rezervari):
                    id1 = filme[i].id_entity
                    id2 = filme[j].id_entity
                    filme[i].id_entity = id2
                    self.film_repository.update(filme[i])
                    filme[j].id_entity = id1
                    self.film_repository.update(filme[j])
            return filme
