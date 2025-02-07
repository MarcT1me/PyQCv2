from dataclasses import dataclass, field
from typing import Self

import Engine
from Engine.data import MetaData
from Engine.math import vec2
from Engine.data.config import Win


@dataclass
class WinData(MetaData):
    """ data for every engine window """
    size: vec2 = field(default_factory=lambda: vec2(Win.size))
    name: str = field(default_factory=lambda: Win.name)
    monitor: int | None = field(default_factory=lambda: Win.monitor)
    vsync: int = field(default_factory=lambda: Win.vsync)
    full: bool = field(default_factory=lambda: Win.full)
    is_desktop: bool = field(default_factory=lambda: Win.is_desktop)
    flags: int = field(default_factory=lambda: Win.flags)

    def extern(self, changes: dict) -> Self:
        """ extern ths win_data and return new """
        [setattr(self, var, value) for var, value in changes.items()]
        return self

    def to_kwargs(self):
        kwargs = {
            'size': self.size,
            'flags': self.flags,
            'vsync': self.vsync,
        }
        if self.monitor not in (None, Engine.EMPTY) and str(self.monitor) not in 'nullEmptyType':
            kwargs['display'] = self.monitor
        return kwargs
