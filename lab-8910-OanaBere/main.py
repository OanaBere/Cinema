from Domain.card_client_validator import CardClientValidator
from Domain.film_validator import FilmValidator
from Domain.rezervare_validator import RezervareValidator
from Repository.json_repository import JsonRepository
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService
from UserInterface.Console import Console


def main():

    undo_redo_service = UndoRedoService()
    film_repository = JsonRepository('films.json')
    film_validator = FilmValidator()
    film_service = FilmService(film_repository, film_validator,
                               undo_redo_service)
    card_client_repository = JsonRepository('cards.json')
    card_client_validator = CardClientValidator()
    card_client_service = CardClientService(card_client_repository,
                                            card_client_validator,
                                            undo_redo_service)
    rezervare_repository = JsonRepository('rezervari.json')
    rezervare_validator = RezervareValidator()
    rezervare_service = RezervareService(rezervare_repository,
                                         rezervare_validator,
                                         film_repository,
                                         card_client_repository,
                                         undo_redo_service)

    console = Console(film_service, card_client_service, rezervare_service,
                      undo_redo_service)
    console.run_console()


if __name__ == '__main__':
    main()
