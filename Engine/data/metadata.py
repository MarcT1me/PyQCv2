from uuid import uuid4
from dataclasses import dataclass, field
from typing import Optional, Self


@dataclass
class MetaData:
    name: Optional[str] = None
    id: str = field(default_factory=uuid4)

    def extern(self, changes: dict) -> Self:
        """ extern ths win_data and return new """
        [setattr(self, var, value) for var, value in changes.items()]
        return self
