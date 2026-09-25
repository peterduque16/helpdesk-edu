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
