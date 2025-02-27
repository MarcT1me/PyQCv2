from uuid import uuid4, UUID
from dataclasses import dataclass, field
from typing import Optional, Hashable


@dataclass
class Identifier(Hashable):
    name: Optional[str] = None
    uuid: UUID = field(init=False, default_factory=uuid4)

    def __str__(self):
        return str(self.name if self.name else self.uuid)

    def __repr__(self):
        return f"Identifier<{self.__str__()}>"

    def __hash__(self):
        return int(self.uuid)
