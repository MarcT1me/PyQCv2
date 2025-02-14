from dataclasses import dataclass, field

from Engine.data import MetaData, WinDefault
from Engine.math import vec2


@dataclass
class WinData(MetaData):
    """ data for every engine window """
    size: vec2 = field(default_factory=lambda: vec2(WinDefault.size))
    name: str = field(default_factory=lambda: WinDefault.name)
    monitor: int | None = field(default_factory=lambda: WinDefault.monitor)
    vsync: int = field(default_factory=lambda: WinDefault.vsync)
    full: bool = field(default_factory=lambda: WinDefault.full)
    is_desktop: bool = field(default_factory=lambda: WinDefault.is_desktop)
    flags: int = field(default_factory=lambda: WinDefault.flags)

    def to_kwargs(self):
        kwargs = {
            'size': self.size,
            'flags': self.flags,
            'vsync': self.vsync,
        }
        if self.monitor is not None:
            kwargs['display'] = self.monitor
        return kwargs
