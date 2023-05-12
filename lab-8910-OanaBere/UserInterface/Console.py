from Domain.exceptions import NegativeValueError, DateError, NegativeId, \
    NotInProgram, HourError
from Domain.movie_generator import MovieGenerator
from Repository.exceptions import NoSuchIdError, DuplicateIdError
from Service.card_client_service import CardClientService
from Service.film_service import FilmService
from Service.rezervare_service import RezervareService
from Service.undo_redo_service import UndoRedoService


class Console:
    def __init__(self,
                 film_service: FilmService,
                 card_client_service: CardClientService,
                 rezervare_service: RezervareService,
                 undo_redo_service: UndoRedoService):
        self.film_service = film_service
        self.card_client_service = card_client_service
        self.rezervare_service = rezervare_service
        self.undo_redo_service = undo_redo_service

    def show_menu(self):
        print('a[film|card|rez] - adaugare film sau card client'
              ' sau rezervare.')
        print('u[film|card|rez] - update film sau card client sau rezervare.')
        print('d[film|card|rez] - delete film sau card client sau rezervare.')
        print('s[film|card|rez] - show all filme sau carduri client sau'
              ' rezervari.')
        print('1. Afisarea cardurilor in ordine descrescatoare dupa'
              ' numarul de puncte acumulate')
        print('2. Generator random pentru o entitate')
        print('3. Căutare filme și clienți. Căutare full text.')
        print('4. Afișarea tuturor rezervărilor dintr-un interval de ore dat')
        print('5. Afișarea filmelor ordonate descrescător după numărul de'
              ' rezervări.')
        print('6. Ștergerea tuturor rezervărilor dintr-un anumit interval de'
              ' zile.')
        print('7. Incrementarea cu o valoare dată a punctelor de pe toate'
              ' cardurile a căror zi de naștere se află într-un interval dat.')
        print('a. Undo')
        print('b. Redo')
        print('x. Iesire')

    def run_console(self):
        while True:
            self.show_menu()
            opt = input('Alegeti optiunea: ')

            if opt == 'afilm':
                self.handle_add_film()
            elif opt == 'acard':
                self.handle_add_card()
            elif opt == 'arez':
                self.handle_add_rezervare()

            elif opt == 'ufilm':
                self.handle_update_film()
            elif opt == 'ucard':
                self.handle_update_card_client()
            elif opt == 'urez':
                self.handle_update_rezervare()

            elif opt == 'dfilm':
                self.handle_delete_film()
            elif opt == 'dcard':
                self.handle_delete_card_client()
            elif opt == 'drez':
                self.handle_delete_rezervare()

            elif opt == 'sfilm':
                self.handle_show_all(self.film_service.show_all_films())
            elif opt == 'scard':
                self.handle_show_all(self.card_client_service.show_all_cards())
            elif opt == 'srez':
                self.handle_show_all(self.rezervare_service.show_all_rezervari
                                     ())
            elif opt == '1':
                result = self.card_client_service.sort_cards()
                print(result)
            elif opt == '2':
                self.handle_generate_movie()
            elif opt == '3':
                self.handle_cautare_full_text(
                    self.film_service.show_all_films(),
                    self.card_client_service.show_all_cards())
            elif opt == '4':
                self.handle_rezervari_din_interval(self.rezervare_service.
                                                   show_all_rezervari())
            elif opt == '5':
                self.handle_ord_desc_nr_rezervari(
                    self.film_service.show_all_films(),
                    self.rezervare_service.show_all_rezervari())
            elif opt == '6':
                self.handle_stergere_rezervare_din_interval(
                    self.rezervare_service.show_all_rezervari())
            elif opt == '7':
                self.handle_incrementare_puncte_inteval_zi_nastere(
                    self.card_client_service.show_all_cards())
            elif opt == 'a':
                self.undo_redo_service.do_undo()
            elif opt == 'b':
                self.undo_redo_service.do_redo()
            elif opt == 'x':
                break
            else:
                print('Optiune invalida!')

    def handle_add_film(self):
        try:
            id_film = input('Dati id-ul filmului: ')
            titlu = input('Dati titlul filmului: ')
            an_aparitie = int(input('Dati anul aparitiei: '))
            pret_bilet = float(input('Dati pretul biletului: '))
            in_program = input('da - daca este in program, nu - daca'
                               ' nu se afla in program')
            self.film_service.add_film(id_film, titlu, an_aparitie,
                                       pret_bilet, in_program)
        except NegativeId as ni:
            print('Eroare id negativ:', ni)
        except DateError as de:
            print('Eroare an negativ:', de)
        except NegativeValueError as nve:
            print('Eroare pret negativ:', nve)
        except DuplicateIdError as die:
            print('Eroare de ID:', die)
        except NotInProgram as nip:
            print('Eroare valoare:', nip)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_add_card(self):
        try:
            id_card_client = input('Dati id-ul cardului: ')
            nume = input('Dati numele titularului de card: ')
            prenume = input('Dati prenumele titularului de card: ')
            cnp = str(input('Dati cnp-ul persoanei: '))
            data_nastere = input('Dati data de nastere a persoanei'
                                 ' (DD-MM-YYYY)')
            data_inregistrarii = input('Dati data inregistrarii clientului'
                                       ' (DD-MM-YYYY): ')
            puncte_acumulate = int(input('Dati numarul punctelor acumulate'))
            self.card_client_service.add_card(id_card_client, nume, prenume,
                                              cnp, data_nastere,
                                              data_inregistrarii,
                                              puncte_acumulate)
        except NegativeId as ni:
            print('Eroare de id negativ:', ni)
        except DateError as de:
            print('Eroare data introdusa gresit:', de)
        except NegativeValueError as nve:
            print('Eroare puncte negative:', nve)
        except DuplicateIdError as die:
            print('Eroare de ID:', die)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_add_rezervare(self):
        try:
            id_rezervare = input('Dati id-ul rezervarii: ')
            id_film = input('Dati id-ul filmului: ')
            id_card_client = input('Dati id-ul cardului: ')
            data = input('Dati data: ')
            ora = input('Dati ora: ')
            card = self.card_client_service.card_client_repository \
                .read(id_card_client)
            film = self.film_service.film_repository.read(id_film)

            self.rezervare_service.add_rezervare(id_rezervare, id_film,
                                                 id_card_client, data, ora)
            puncte_acumulate = int(card.puncte_acumulate + 0.1 *
                                   film.pret_bilet)
            print(f' Numarul punctelor acumulate pe card este:'
                  f' {puncte_acumulate}')
        except NegativeId as ni:
            print('Eroare de id negativ:', ni)
        except DateError as de:
            print('Eroare de data incorect introdusa:', de)
        except HourError as he:
            print('Eroare de ora incorect introdusa:', he)
        except DuplicateIdError as die:
            print('Eroare ID duplicat:', die)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_film(self):

        try:
            id_film = input('Dati id-ul filmului: ')
            titlu = input('Dati titlul filmului: ')
            an_aparitie = int(input('Dati anul aparitiei filmului: '))
            pret_bilet = float(input('Dati pretul biletului: '))
            in_program = input('da - daca filmul este in program,'
                               ' nu - in sens contrar: ')

            self.film_service.update_film(id_film, titlu, an_aparitie,
                                          pret_bilet, in_program)

        except NegativeId as ni:
            print('Eroare id negativ:', ni)
        except DateError as nye:
            print('Eroare an negativ:', nye)
        except NegativeValueError as nve:
            print('Eroare pret negativ:', nve)
        except DuplicateIdError as die:
            print('Eroare de ID:', die)
        except NotInProgram as nip:
            print('Eroare valoare:', nip)
        except NoSuchIdError as nsie:
            print('Eroare de id: id inexistent: ', nsie)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_card_client(self):
        try:
            id_card_client = input('Dati id-ul cardului: ')
            nume = input('Dati numele clientului: ')
            prenume = input('Dati prenumele clientului: ')
            cnp = input('Dati cnp-ul clientului: ')
            data_nasterii = input('Dati data nasterii clientului: ')
            data_inregistrarii = input('Dati data inregistrarii clientului: ')
            puncte_acumulate = int(input('Dati numarul punctelor acumulate: '))

            self.card_client_service.update_card(id_card_client, nume, prenume,
                                                 cnp, data_nasterii,
                                                 data_inregistrarii,
                                                 puncte_acumulate)
        except NegativeId as ni:
            print('Eroare de id negativ:', ni)
        except DateError as de:
            print('Eroare data introdusa gresit:', de)
        except NoSuchIdError as nsie:
            print('Eroare de id: id inexistent: ', nsie)
        except NegativeValueError as nve:
            print('Eroare puncte negative:', nve)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_update_rezervare(self):
        try:
            id_rezervare = input('Dati id-ul rezervarrii: ')
            id_film = input('Dati id-ul filmului: ')
            id_card_client = input('Dati id-ul cardului: ')
            data = input('Dati data: ')
            ora = input('Dati ora: ')

            self.rezervare_service.update_rezervare(id_rezervare, id_film,
                                                    id_card_client, data, ora)
        except NegativeId as ni:
            print('Eroare de id negativ:', ni)
        except DateError as de:
            print('Eroare de data incorect introdusa:', de)
        except HourError as he:
            print('Eroare de ora incorect introdusa:', he)
        except NoSuchIdError as nsie:
            print('Eroare de ID:', nsie)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_film(self):

        try:
            film_id_to_delete = input('Da id-ul filmului pe care vrei sa'
                                      ' il stergi: : ')
            cc_id_sters = ''
            self.film_service.delete_film(film_id_to_delete)
            self.rezervare_service.delete_in_cascada_film(
                self.rezervare_service.show_all_rezervari(),
                film_id_to_delete,
                cc_id_sters)
        except NoSuchIdError as nsie:
            print('Eroare de ID:', nsie)
        except NegativeId as ni:
            print('Eroare id negativ:', ni)
        except DateError as de:
            print('Eroare an negativ:', de)
        except NegativeValueError as nve:
            print('Eroare pret negativ:', nve)
        except DuplicateIdError as die:
            print('Eroare de ID:', die)
        except NotInProgram as nip:
            print('Eroare valoare:', nip)
        except Exception as ex:
            print('Eroare:', ex)

    def handle_delete_card_client(self):
        try:
            cc_id_to_delete = input('Da id-ul cardului clientului pe'
                                    ' care vrei sa il stergi: : ')
            id_film_sters = ''
            self.card_client_service.delete_card(cc_id_to_delete)
            self.rezervare_service.delete_in_cascada_film(
                self.rezervare_service.show_all_rezervari(),
                id_film_sters, cc_id_to_delete)
        except ValueError as ve:
            print('Eroare de validare: ', ve)
        except KeyError as ke:
            print('Eroare de cheie: ', ke)
        except Exception as ex:
            print('Eroare: ', ex)

    def handle_delete_rezervare(self):
        try:
            rezervarea_id_to_delete = input('Dati id-ul rezervarii pe care'
                                            ' doriti sa o stergeti: : ')
            self.rezervare_service.delete_rezervare(rezervarea_id_to_delete)
        except NegativeId as ni:
            print('Eroare de id negativ:', ni)
        except DateError as de:
            print('Eroare data introdusa gresit:', de)
        except NegativeValueError as nve:
            print('Eroare puncte negative:', nve)
        except NoSuchIdError as nsie:
            print('Eroare de ID:', nsie)
        except Exception as ex:
            print('Eroare: ', ex)

    def handle_show_all(self, objects):
        for obj in objects:
            print(obj)

    def handle_generate_movie(self):
        movie_generator = MovieGenerator(self.film_service)
        number_of_movies_str = input('Cate filme doriti sa generati?')
        try:
            if not number_of_movies_str.isdigit():
                raise ValueError('Numarul trebuie sa fie de tip intreg!')
            number_of_movies_int = int(number_of_movies_str)
            movie_generator.generate_movie(number_of_movies_int)
            print(f'Au fost generate {number_of_movies_int} filme random.')
        except ValueError as ve:
            print('Eroare', ve)

    def handle_cautare_full_text(self, filme, carduri_clieti):

        """
        Afiseaza doua liste cu toate filmele, respectiv cardurile clientilor
        care au o valoare in care se gaseste un sir dat de la tastatura
        :param filme: filmele in care cautam
        :param carduri_clieti: cardurile intre care cautam
        :return: cele doua liste de filme, respectiv carduri, ce contin sirul
        """

        sir = input('Dati grupul de simboluri pe care sa il contina filmele si'
                    ' cardurile clientilor: ')

        print(self.film_service.cautare_full_text_filme(filme, sir))
        print(self.card_client_service.cautare_full_text_carduri_clienti(
            carduri_clieti, sir))

    def handle_rezervari_din_interval(self, rezervari):

        """
        Afiseaza toate rezervarile din memorie dintr-un interval orar
        :param rezervari: rezervarile din memorie
        :return: - lista de rezervari
                 - erorile aferente
        """

        lista = []
        hstart = input('Dati ora de inceput de forma hh:mm:ss : ')
        hfinal = input('Dati ora de final de forma hh:mm:ss : ')
        try:
            for rezervare in rezervari:
                if self.rezervare_service.rezervare_din_interval(rezervare,
                                                                 hstart,
                                                                 hfinal) is \
                        not None:
                    lista.append(rezervare)
            print(lista)
        except HourError as he:
            print('Eroare de ora introdusa incorect: ', he)
        except Exception as ex:
            print('Eroare: ', ex)

    def handle_ord_desc_nr_rezervari(self, filme, rezervari):

        """
        Afiseaza filmele ordonate descrescator dupa numarul lor de rezervari
        :param filme: filmele
        :param rezervari: rezervarile
        :return: - lista de filme ordonata sau
                 - erorole aferente
        """

        try:
            print(self.film_service.ordonare_dupa_nr_rezervari(filme,
                                                               rezervari))
        except Exception as ex:
            print('Eroare: ', ex)

    def handle_stergere_rezervare_din_interval(self, rezervari):

        """
        Sterge rezervarile dintr-un interval de zile
        :param rezervari: rezervarile
        :return: - exceptiile aferente(daca exista)
        """

        datastart = input('Dati data de inceput: ')
        datafinal = input('Dati data de sfarsit: ')
        try:
            self.rezervare_service.stergere_rezervare_din_interval(rezervari,
                                                                   datastart,
                                                                   datafinal)
            print('Rezervari sterse cu succes!')
        except DateError as de:
            print('Eroare de data introdusa incorect: ', de)
        except Exception as ex:
            print('Eroare: ', ex)

    def handle_incrementare_puncte_inteval_zi_nastere(self, carduri_clienti):

        """
        Incrementeaza punctele acumulate pe card, daca ziua nasterii
         proprietarului se afla intr-un interval citit
        :param carduri_clienti: cardurile
        :return: - erorile aferente (daca exista)
        """

        datastart = input('Dati data de inceput: ')
        datafinal = input('Dati data de sfarsit: ')
        try:
            self.card_client_service.incrementare_puncte_inteval_zi_nastere(
                carduri_clienti, datastart, datafinal)
            print('Incrementarile au fost realizate cu succes!')
        except DateError as de:
            print('Eroare de data introdusa incorect: ', de)
