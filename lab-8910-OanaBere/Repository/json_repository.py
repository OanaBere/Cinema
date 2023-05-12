from typing import Dict, Type, Union, Optional, List

import jsonpickle

from Domain.entity import Entity
from Repository.exceptions import DuplicateIdError, NoSuchIdError
from Repository.repository import Repository


class JsonRepository(Repository):

    def __init__(self, filename):
        self.filename = filename

    def __read_file(self):
        try:
            with open(self.filename, 'r') as f:
                return jsonpickle.loads(f.read())
        except Exception:
            return {}

    def __write_file(self, objects: Dict[str, Entity]):
        with open(self.filename, 'w') as f:
            f.write(jsonpickle.dumps(objects))

    def create(self, entity: Entity) -> None:
        """
        Creeaza o noua entitate in memorie
        :param entity: entitatea de adaugat
        :return: eroare daca id-ul entitatii exista deja in memorie
        """

        entities = self.__read_file()
        if self.read(entity.id_entity) is not None:
            raise DuplicateIdError(f'Exista deja o entitate cu '
                                   f'id-ul {entity.id_entity}.')

        entities[entity.id_entity] = entity
        self.__write_file(entities)

    def read(self, id_entity: object = None) -> Type[Union[Optional[Entity],
                                                           List[Entity]]]:
        """
        Afla entitatea data printr-un id
        :param id_entity: id-ul entitatii
        :return:
            - entitatea cu id=id_entity sau None daca id_entity nu e None
            - lista cu toate entitatile daca id_entity e None
        """

        entities = self.__read_file()
        if id_entity:
            if id_entity in entities:
                return entities[id_entity]
            else:
                return None

        return list(entities.values())

    def update(self, entity: Entity) -> None:
        """
        TODO
        :param entity:
        :return:
        """

        entities = self.__read_file()
        if self.read(entity.id_entity) is None:
            msg = f'Nu exista o entitate cu id-ul {entity.id_entity} ' \
                  f'de actualizat.'
            raise NoSuchIdError(msg)

        entities[entity.id_entity] = entity
        self.__write_file(entities)

    def delete(self, id_entity: str) -> None:
        """
        TODO
        :param id_entity:
        :return:
        """
        entities = self.__read_file()
        if self.read(id_entity) is None:
            raise NoSuchIdError(
                f'Nu exista o entitate cu id-ul {id_entity} pe care sa'
                f' o stergem.')

        del entities[id_entity]
        self.__write_file(entities)
