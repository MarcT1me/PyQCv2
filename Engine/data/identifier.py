from typing import TypeAlias, Tuple, Hashable, Optional, Self
from dataclasses import dataclass, field
from uuid import UUID, uuid4

IdentifierType: TypeAlias = 'str | Tuple[str, UUID] | Identifier'


@dataclass
class Identifier(Hashable):
    name: Optional[str] = None
    uuid: UUID = field(init=False, default_factory=uuid4)

    @classmethod
    def from_uncertain(cls, value: IdentifierType) -> Self:
        """ create Identifier from uncertain value
        Examples:
              * Identifier.from_uncertain(some_name)
              * Identifier.from_uncertain(some_name, some_uuid)
              * Identifier.from_uncertain(already_exist_identifier)"""
        if isinstance(value, Identifier):
            return value
        elif isinstance(value, str):
            return cls(value)
        else:
            return cls(*value)

    def __str__(self):
        return str(self.name if self.name else self.uuid)

    def __repr__(self):
        return f"Identifier<{self.__str__()}>"

    def __hash__(self):
        return int(self.uuid)
