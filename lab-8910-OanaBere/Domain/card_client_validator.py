from datetime import datetime

from Domain.card_client import CardClient
from Domain.exceptions import NegativeId, DateError, NegativeValueError


class CardClientValidator:
    def validate(self, card_client: CardClient):

        if int(card_client.id_entity) <= 0:
            raise NegativeId(
                    'Id-ul cardului trebuie sa fie mai mare ca 0!')

        if len(card_client.cnp) != 13:
            raise ValueError('CNP invalid. Trebuie sa fie de 13 caractere!')

        if card_client.data_nastere != datetime.strptime(
                card_client.data_nastere, "%d-%m-%Y").strftime('%d-%m-%Y'):
            raise DateError(
                'Format invalid data! Trebuie sa fie DD-MM-YYYY')

        if card_client.data_inregistrarii != datetime.strptime(
                card_client.data_inregistrarii, "%d-%m-%Y"). \
                strftime('%d-%m-%Y'):
            raise DateError(
                'Format invalid data! Trebuie sa fie DD-MM-YYYY')

        if int(card_client.puncte_acumulate) < 0:
            raise NegativeValueError(
                'Punctele trebuie sa fie mai mare ca 0')
