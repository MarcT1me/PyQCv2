from uuid import uuid4
from dataclasses import dataclass, field
from typing import Self
import Engine


@dataclass
class MetaDate:
    id: str = field(default_factory=uuid4)
    time_stamp: int = field(default_factory=Engine.timing.Clock.get_ticks)

    def extern(self, changes: dict) -> Self:
        """ extern ths win_data and return new """
        for var, value in changes.items():
            exec(f"self.{var} = value")
            exec(f"Engine.data.Win.{var} = value")
        return self