from uuid import uuid4
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MetaData:
    name: Optional[str] = None
    id: str = field(default_factory=uuid4)
