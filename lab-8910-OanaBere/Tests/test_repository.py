from Domain.card_client import CardClient
from Domain.film import Film
from Domain.rezervare import Rezervare
from Repository.json_repository import JsonRepository
from utils import clear_file


def test_card_repository():

    filename = 'test_card.json'
    clear_file(filename)
    card_client_repository = JsonRepository(filename)
    added = CardClient('1', 'Pop', 'Ion', '5020391256751', '20-03-1999',
                       '10-03-2019', 3)
    card_client_repository.create(added)
    assert card_client_repository.read(added.id_entity) == added
    card_client_repository.update(CardClient('1', 'Popescu', 'Ioana',
                                             '6021945389712', '13.05.2001',
                                             '29.07.2020', 0))
    assert card_client_repository.read('1').nume == 'Popescu'
    assert card_client_repository.read('1').prenume == 'Ioana'
    assert card_client_repository.read('1').data_inregistrarii == '29.07.2020'
    card_client_repository.delete('1')
    assert card_client_repository.read('1') is None


def test_film_repository():

    filename = 'test_films.json'
    clear_file(filename)
    film_repository = JsonRepository(filename)
    added = Film('1', 'Titanic', 2000, 30, 'da')
    film_repository.create(added)
    assert film_repository.read(added.id_entity) == added
    film_repository.update(Film('1', 'Lord of the Rings', 2013, 17.5, 'da'))
    assert film_repository.read('1').titlu == 'Lord of the Rings'
    assert film_repository.read('1').an_aparitie == 2013
    assert film_repository.read('1').pret_bilet == 17.5
    film_repository.delete('1')
    assert film_repository.read('1') is None


def test_rezervare_repository():

    filename = 'test_rezervare.json'
    clear_file(filename)
    rezervare_repository = JsonRepository(filename)
    added = Rezervare('1', '2', '3', '12-11-2021', '12:30:47')
    rezervare_repository.create(added)
    assert rezervare_repository.read(added.id_entity) == added
    rezervare_repository.update(Rezervare('1', '2', '3', '12-12-2021',
                                          '12:15:00'))
    assert rezervare_repository.read('1').data == '12-12-2021'
    assert rezervare_repository.read('1').ora == '12:15:00'
    rezervare_repository.delete('1')
    assert rezervare_repository.read('1') is None


def teste():

    test_film_repository()
    test_rezervare_repository()
    test_card_repository()
