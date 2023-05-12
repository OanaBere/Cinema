from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class CardClient(Entity):
    nume: str
    prenume: str
    cnp: str
    data_nastere: str
    data_inregistrarii: str
    puncte_acumulate: int
