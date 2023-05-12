from datetime import datetime

from Domain.exceptions import NegativeId, DateError, HourError
from Domain.rezervare import Rezervare


class RezervareValidator:
    def validate(self, rezervare: Rezervare):
        """
        verifica daca rezervarea este valida
        :param rezervare: rezervarea
        :return: o posibila eroare
        """
        if int(rezervare.id_entity) <= 0:
            raise NegativeId('Id-ul rezervarii trebuie sa fie mai mare decat'
                             ' 0!')

        if int(rezervare.id_film) <= 0:
            raise NegativeId('Id-ul filmului rezervat trebuie sa fie mai mare'
                             ' ca 0!')

        if int(rezervare.id_card_client) <= 0:
            raise NegativeId('Id-ul cardului trebuie sa fie mai mare decat 0!')

        if rezervare.data != datetime.strptime(rezervare.data, "%d-%m-%Y"). \
                strftime('%d-%m-%Y'):
            raise DateError('Format invalid data! Trebuie sa fie de forma'
                            'DD-MM-YYYY!')

        if rezervare.ora != datetime.strptime(rezervare.ora, "%H:%M:%S"). \
                strftime("%H:%M:%S"):
            raise HourError('Format ora invalid! Trebuie sa fie de'
                            ' forma HH:MM:SS')
