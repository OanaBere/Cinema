from datetime import datetime
from typing import List, Optional

from Domain.add_operation import AddOperation
from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.exceptions import DateError
from Repository.repository import Repository
from Service.undo_redo_service import UndoRedoService


class CardClientService:
    def __init__(self,
                 card_client_repository: Repository,
                 card_client_validator: CardClientValidator,
                 undo_redo_service: UndoRedoService):
        self.card_client_repository = card_client_repository
        self.card_client_validator = card_client_validator
        self.undo_redo_service = undo_redo_service

    def add_card(self,
                 id_card_client: str,
                 nume: str,
                 prenume: str,
                 cnp: str,
                 data_nastere: str,
                 data_inregistrarii: str,
                 puncte_acumulate: int):
        """
        functie de adaugare a unui nou card

        """

        card_client = CardClient(id_card_client, nume, prenume, cnp,
                                 data_nastere,
                                 data_inregistrarii, puncte_acumulate)
        self.card_client_validator.validate(card_client)
        self.card_client_repository.create(card_client)

        self.undo_redo_service.clear_redo()
        add_operation = AddOperation(self.card_client_repository, card_client)
        self.undo_redo_service.add_to_undo(add_operation)

    def update_card(self,
                    id_card_client: str,
                    nume: str,
                    prenume: str,
                    cnp: str,
                    data_nastere: str,
                    data_inregistrarii: str,
                    puncte_acumulate: int):
        """
        functie de actualiat carduri
        :param id_card_client: str
        :param nume: str
        :param prenume: str
        :param cnp: str
        :param data_nastere: str
        :param data_inregistrarii: str
        :param puncte_acumulate: int
        :return: cardul actualizat
        """

        card_client = CardClient(id_card_client, nume, prenume, cnp,
                                 data_nastere,
                                 data_inregistrarii, puncte_acumulate)
        self.card_client_validator.validate(card_client)
        self.card_client_repository.update(card_client)

    def delete_card(self, id_card_client: str):
        self.card_client_repository.delete(id_card_client)

    def show_all_cards(self) -> List[CardClient]:
        return self.card_client_repository.read()

    def show_card(self, id_card_client: str) -> Optional[CardClient]:
        return self.card_client_repository.read(id_card_client)

    def sort_cards(self):
        """
        functie de sortare a cardurilor, in ord descresc, dupa nr de puncte
        :return: lista de cardurile sortate
        """
        result = []
        cards = self.show_all_cards()
        n = len(cards)
        for i in range(0, n - 1):
            for j in range(i + 1, n):
                if cards[i].puncte_acumulate < cards[j].puncte_acumulate:
                    aux = cards[i]
                    cards[i] = cards[j]
                    cards[j] = aux
        result.append(cards)
        return result

    def cautare_full_text_card_client(self, card_client, sir):

        """
        Cauta in orice valoare a cheilor cardului clientului, un sir dat
        :param card_client: cardul clientului
        :param sir: sirul dat
        :return: - card_client - daca s-a gasit sirul sir in card_client
                 - None - daca nu s-a gasit sirul in card_client
        """

        if sir in card_client.id_entity:
            return card_client

        if sir in card_client.nume:
            return card_client

        if sir in card_client.prenume:
            return card_client

        if sir in card_client.cnp:
            return card_client

        if sir in card_client.data_nastere:
            return card_client

        if sir in card_client.data_inregistrarii:
            return card_client

        if sir in str(card_client.puncte_acumulate):
            return card_client

        return None

    def cautare_full_text_carduri_clienti(self, carduri_clienti, sir):

        """
        Creeaza o lista cu toate cardurile clientilor dintr-o lista data in
         care se gaseste un sir dat
        :param carduri_clienti: lista de carduri
        :param sir: sirul dat
        :return: lista de carduri in care se gaseste sir
        """

        lista = []
        for card_client in carduri_clienti:
            if self.cautare_full_text_card_client(card_client, sir) is \
                    not None:
                lista.append(card_client)

        return lista

    def incrementare_puncte_inteval_zi_nastere(self, carduri_clienti,
                                               datastart,
                                               datafinal):

        """
        Adauga un punct la punctele acomulate de pe cardurile clientilor
        care au data nasterii intr-un interval dat
        :param carduri_clienti: lista de carduri
        :param datastart: data de inceput
        :param datafinal: data de sfarsit
        :return: lista de carduri cu punctele acumulate modificate
        """

        if datastart != datetime.strptime(datastart, "%d-%m-%Y"). \
                strftime('%d-%m-%Y'):
            raise DateError('Format invalid data! Trebuie sa fie de forma'
                            'DD-MM-YYYY!')
        if datafinal != datetime.strptime(datafinal, "%d-%m-%Y"). \
                strftime('%d-%m-%Y'):
            raise DateError('Format invalid data! Trebuie sa fie de forma'
                            'DD-MM-YYYY!')

        for card_client in carduri_clienti:
            if int(datastart[6:10]) < int(card_client.data_nastere[6:10]) < \
                    int(datafinal[6:10]):
                card_client.puncte_acumulate = card_client.puncte_acumulate + 1
                self.card_client_repository.update(card_client)

            elif int(card_client.data_nastere[6:10]) == int(datastart[6:10]):
                if int(card_client.data_nastere[3:5]) > int(datastart[3:5]):
                    card_client.puncte_acumulate = \
                        card_client.puncte_acumulate + 1
                    self.card_client_repository.update(card_client)
                else:
                    if int(card_client.data_nastere[3:5]) == \
                            int(datastart[3:5]) and \
                            int(card_client.data_nastere[0:2]) >= \
                            int(datastart[0:2]):
                        card_client.puncte_acumulate = \
                            card_client.puncte_acumulate + 1
                        self.card_client_repository.update(card_client)

            else:
                if int(card_client.data_nastere[6:10]) == \
                        int(datafinal[6:10]):
                    if int(card_client.data_nastere[3:5]) < \
                            int(datafinal[3:5]):
                        card_client.puncte_acumulate = \
                            card_client.puncte_acumulate + 1
                        self.card_client_repository.update(card_client)
                    else:
                        if int(card_client.data_nastere[3:5]) == \
                                int(datafinal[3:5]) and \
                                int(card_client.data_nastere[0:2]) <= \
                                int(datafinal[0:2]):
                            card_client.puncte_acumulate = \
                                card_client.puncte_acumulate + 1
                            self.card_client_repository.update(card_client)

        return carduri_clienti
