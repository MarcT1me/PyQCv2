from uuid import uuid4
from dataclasses import dataclass, field
import Engine


@dataclass
class MetaData:
    name: str = ""
    id: str = field(default_factory=uuid4)
    time_stamp: float = field(default_factory=Engine.timing.uix_time)