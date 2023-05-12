from dataclasses import dataclass

from Domain.entity import Entity


@dataclass
class Film(Entity):
    titlu: str
    an_aparitie: int
    pret_bilet: float
    in_program: str
