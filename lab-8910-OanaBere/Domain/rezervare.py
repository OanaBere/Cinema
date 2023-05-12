from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Rezervare(Entity):
    id_film: str
    id_card_client: str
    data: str
    ora: str
