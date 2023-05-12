from datetime import datetime
from typing import List, Optional

from Domain.add_operation import AddOperation
from Domain.exceptions import HourError, DateError
from Domain.rezervare import Rezervare
from Domain.rezervare_validator import RezervareValidator
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class RezervareService:
    def __init__(self,
                 rezervare_repository: Repository,
                 rezervare_validator: RezervareValidator,
                 film_repository: Repository,
                 card_client_repository: Repository,
                 undo_redo_service: UndoRedoService):

        self.rezervare_repository = rezervare_repository
        self.rezervare_validator = rezervare_validator
        self.film_repository = film_repository
        self.card_client_repository = card_client_repository
        self.undo_redo_service = undo_redo_service

    def add_rezervare(self,
                      id_rezervare: str,
                      id_film: str,
                      id_card_client: str,
                      data: str,
                      ora: str):
        """
        functia adauga o noua rezervare la lista de rezervari deja existente
        """

        if self.film_repository.read(id_film) is None:
            raise KeyError(f'Nu exista niciun film cu id-ul {id_film}')
        if self.card_client_repository.read(id_card_client) is None:
            raise KeyError(f'Nu exista niciun card cu id-ul {id_card_client}')

        film = self.film_repository.read(id_film)
        card_client = self.card_client_repository.read(id_card_client)

        if film.in_program == 'nu':
            raise KeyError(f'Filmul cu id-ul {id_film} nu este in program!')
        else:
            rezervare = Rezervare(id_rezervare, id_film, id_card_client, data,
                                  ora)
            card_client.puncte_acumulate = card_client.puncte_acumulate + \
                film.pret_bilet // 10
            self.card_client_repository.update(card_client)
            self.rezervare_validator.validate(rezervare)
            self.rezervare_repository.create(rezervare)

            self.undo_redo_service.clear_redo()
            add_operation = AddOperation(self.rezervare_repository,
                                         rezervare)
            self.undo_redo_service.add_to_undo(add_operation)

    def update_rezervare(self,
                         id_rezervare: str,
                         id_film: str,
                         id_card_client: str,
                         data: str,
                         ora: str):
        """
        functia actualizeaza o rezervare existenta
        """
        rezervare = Rezervare(id_rezervare, id_film, id_card_client, data, ora)
        self.rezervare_validator.validate(rezervare)
        self.rezervare_repository.update(rezervare)

    def delete_rezervare(self, id_rezervare: str):
        """
        functia sterge o rezervare existenta
        :param id_rezervare: id-ul rezervarii
        :return: -
        """
        self.rezervare_repository.delete(id_rezervare)

    def show_all_rezervari(self) -> List[Rezervare]:
        """
        :return: afiseaza toate rezervarile
        """
        return self.rezervare_repository.read()

    def show_rezervare(self, id_rezervare: str) -> Optional[Rezervare]:
        """
        :return: afiseaza rezervarea dorita
        """
        return self.rezervare_repository.read(id_rezervare)

    def delete_in_cascada_film(self, rezervari, id_film_dat: str,
                               id_card_client_dat: str):
        """
        sterge o rezervare la un film sters, sau facuta de un client al carui
        card a fost sters
        :param rezervari: rezervarile
        :param id_film_dat: id-ul filmului sters
        :param id_card_client_dat: id-ul cardului sters
        :return: lista de rezervari fara rezervarile aferente
        filmului/cardului sters
        """
        if len(id_film_dat) != 0:
            for rezervare in rezervari:
                if rezervare.id_film == id_film_dat:
                    self.rezervare_repository.delete(rezervare.id_entity)
        if len(id_card_client_dat) != 0:
            for rezervare in rezervari:
                if rezervare.id_card_client == id_card_client_dat:
                    self.rezervare_repository.delete(rezervare.id_entity)
        return rezervari

    def rezervare_din_interval(self, rezervare: Rezervare, hstart: str,
                               hfinal: str):
        """
        functie care verifica daca rezervarea se afla intr-un anumit interval
        orar dat
        :param rezervare: o rezervare
        :param hstart: ora inceput
        :param hfinal: ora finala
        :return: -
        """
        if hstart != datetime.strptime(hstart, "%H:%M:%S"). \
                strftime("%H:%M:%S"):
            raise HourError('Ora inceput invalida! Trebuie sa fie de'
                            ' forma HH:MM:SS')
        if hfinal != datetime.strptime(hfinal, "%H:%M:%S"). \
                strftime("%H:%M:%S"):
            raise HourError('Ora final invalida! Trebuie sa fie de'
                            ' forma HH:MM:SS')
        if hfinal > rezervare.ora > hstart:
            return self.rezervare_repository.read(rezervare.id_entity)

        return None

    def stergere_rezervare_din_interval(self, rezervari, datastart, datafinal):

        """
        Sterge din momorie rezervarea dintr-un anumit interval de zile
        :param rezervari: rezervarea
        :param datastart: ziua de start
        :param datafinal: ziua de final
        :return: - eroarea - daca datastart sau datafinal nu e valida
                 - lista de rezervari fara rezervarile din intervalul
                 [datastart, datafinal]
        """

        if datastart != datetime.strptime(datastart, "%d-%m-%Y"). \
                strftime('%d-%m-%Y'):
            raise DateError('Format invalid data! Trebuie sa fie de forma'
                            'DD-MM-YYYY!')
        if datafinal != datetime.strptime(datafinal, "%d-%m-%Y"). \
                strftime('%d-%m-%Y'):
            raise DateError('Format invalid data! Trebuie sa fie de forma'
                            'DD-MM-YYYY!')

        for rezervare in rezervari:
            if (int(datastart[0:2]) < int(rezervare.data[0:2]) <
               int(datafinal[0:2])):
                self.rezervare_repository.delete(rezervare.id_entity)

        return self.rezervare_repository.read()
