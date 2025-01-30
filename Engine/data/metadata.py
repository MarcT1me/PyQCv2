from uuid import uuid4
from dataclasses import dataclass, field


@dataclass
class MetaData:
    name: str = ""
    id: str = field(default_factory=uuid4)
