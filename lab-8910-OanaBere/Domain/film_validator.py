from Domain.exceptions import NegativeId, NegativeValueError, NotInProgram
from Domain.film import Film


class FilmValidator:
    def validate(self, film: Film):
        """
        functie care verifica daca filmul este valid
        :param film: filmul
        :return: o posibila eroare
        """
        if int(film.id_entity) <= 0:
            raise NegativeId('Id-ul filmului trebuie sa fie strict pozitiv,'
                             ' mai mare ca 0!')

        if film.pret_bilet < 0:
            raise NegativeValueError('Pretul biletului trebuie sa fie strict'
                                     ' pozitiv!')

        optiuni = ['da', 'nu']
        if film.in_program not in optiuni:
            raise NotInProgram('Variabila in_program trebuie sa fie "da" sau'
                               ' "nu"! ')
