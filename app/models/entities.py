from dataclasses import dataclass, field
from typing import Tuple
from app.domain.errors import ValidationError

@dataclass
class Ticket:
    _tags: list[str] = field(default_factory=list, init=False, repr=False)

    @property
    def tags(self) -> Tuple[str, ...]:
        return tuple(self._tags)

    def add_tag(self, tag: str) -> None:
        normalized = tag.strip().lower()
        if not normalized:
            raise ValidationError("Etiqueta vacía no permitida")
        if normalized in self._tags:
            return
        self._tags.append(normalized)
