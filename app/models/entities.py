from dataclasses import dataclass, field

@dataclass
class User:
    id: str
    name: str

@dataclass
class Ticket:
    id: str
    requester_id: str
    assigned_id: str = None
    _tags: tuple = field(default_factory=tuple, init=False, repr=False)

    @property
    def tags(self):
        return self._tags

    def add_tag(self, tag: str):
        tag = tag.strip()
        if not tag:
            raise ValueError("La etiqueta no puede estar vacía")

        tag = tag.lower()
        if tag not in self._tags:
            self._tags = self._tags + (tag,)
@dataclass
class ArticuloConocimiento:
    id: str
    ticket_id: str
    titulo: str
    solucion: str

    def __post_init__(self):
        if not self.titulo.strip():
            raise ValueError("El título no puede estar vacío")

        if not self.solucion.strip():
            raise ValueError("La solución no puede estar vacía")
