from Domain.card_client import CardClient
from Domain.card_client_validator import CardClientValidator
from Domain.film import Film
from Domain.film_validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from utils import clear_file


def test_service():
    undo_redo_service = UndoRedoService()

    filename = 'test_film.json'
    clear_file(filename)
    film_repository1 = JsonRepository(filename)
    film_validator1 = FilmValidator()

    filename2 = 'test_repository.json'
    clear_file(filename2)
    rezervare_repository1 = JsonRepository(filename2)
    rezervare_validator1 = RezervareValidator()

    filename3 = 'test_card_client.json'
    clear_file(filename3)
    card_client_repository1 = JsonRepository(filename3)
    card_client_validator1 = CardClientValidator()

    card_client_service = CardClientService(card_client_repository1,
                                            card_client_validator1,
                                            undo_redo_service)
    film_service = FilmService(film_repository1, film_validator1,
                               undo_redo_service)
    rezervare_service = RezervareService(rezervare_repository1,
                                         rezervare_validator1,
                                         film_repository1,
                                         card_client_repository1,
                                         undo_redo_service)

    added = Film('1', 'Titanic', 2000, 30, 'da')
    added2 = Film('2', 'House of Gucci', 2020, 22.9, 'da')
    film_service.add_film('1', 'Titanic', 2000, 30, 'da')
    film_service.add_film('2', 'House of Gucci', 2020, 22.9, 'da')
    film_service.add_film('3', 'Dumbo', 2005, 11.9, 'nu')

    card2 = CardClient('2', 'Bob', 'Maria', '6013578928123', '21-03-2000',
                       '04-01-2022', 0)
    card_client_service.add_card('1', 'Miron', 'Paula', '6021928907652',
                                 '29-05-2002', '03-09-2019', 0)
    card_client_service.add_card('2', 'Bob', 'Maria', '6013578928123',
                                 '21-03-2000', '04-01-2022', 0)
    card_client_service.add_card('3', 'Dragomir', 'Tudor', '5021928280008',
                                 '22-10-1998', '30-10-2018', 0)

    rezervare_service.add_rezervare('1', '1', '1', '12-11-2021', '09:45:00')
    rezervare_service.add_rezervare('2', '1', '1', '01-01-2022', '13:50:00')
    rezervare_service.add_rezervare('3', '2', '1', '10-02-2022', '22:10:00')

    # Test pt film_service

    assert film_service.show_film(added.id_entity) == added
    film_service.update_film('1', 'Rapirea 2', 2020, 17, 'da')
    assert film_service.show_film('1').titlu == 'Rapirea 2'
    assert film_service.show_film('1').an_aparitie == 2020
    assert film_service.show_film('1').pret_bilet == 17
    film_service.delete_film('3')
    assert film_service.show_film('3') is None

    lista = rezervare_service.show_all_rezervari()
    assert film_service.numar_rezervari(added2, lista) == 1
    assert film_service.numar_rezervari(film_service.show_film('1'),
                                        lista) == 2
    film_service.ordonare_dupa_nr_rezervari(film_service.show_all_films(),
                                            lista)
    assert len(film_service.show_all_films()) == 2
    assert film_service.show_film('2') == added2

    assert film_service.cautare_full_text_film(film_service.show_film('1'),
                                               '3') is None
    assert film_service.cautare_full_text_film(film_service.show_film('1'),
                                               'da') ==\
           film_service.show_film('1')

    assert film_service.cautare_full_text_filme(film_service.show_all_films(),
                                                'Number') == []

    # Test pt card_client_service

    assert card_client_service.show_card(card2.id_entity) == card2
    card_client_service.update_card('1', 'Pop', 'Iulia',
                                    '6021928907682', '25-09-2002',
                                    '29-09-2021', 10)
    assert card_client_service.show_card('1').prenume == 'Iulia'
    assert card_client_service.show_card('1').puncte_acumulate == 10
    card_client_service.delete_card('3')
    assert card_client_service.show_card('3') is None

    card_nou1 = card_client_service.show_card('1')
    card_client_service.incrementare_puncte_inteval_zi_nastere(
        card_client_service.show_all_cards(), '27-05-2002', '27-08-2002')
    assert card_nou1.puncte_acumulate == card_client_service.show_card('1')\
        .puncte_acumulate - 1

    assert card_client_service.cautare_full_text_carduri_clienti(
        card_client_service.show_all_cards(), 'Number') == []

    # Test pentru rezervare_service

    rezervare_service.update_rezervare('1', '2', '1', '12-12-2021', '12:55:00')
    assert rezervare_service.show_rezervare('1').id_film == '2'
    assert rezervare_service.show_rezervare('1').ora == '12:55:00'
    rezervare_service.delete_rezervare('3')
    assert rezervare_service.show_rezervare('3') is None

    rezervare1_noua = rezervare_service.show_rezervare('1')
    assert rezervare_service.rezervare_din_interval(
        rezervare_service.show_rezervare('1'), '11:59:00',
        '12:59:00') == rezervare1_noua


test_service()
