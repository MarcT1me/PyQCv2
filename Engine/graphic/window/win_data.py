from dataclasses import dataclass, field

import Engine


@dataclass(kw_only=True)
class WinData(Engine.data.MetaData):
    """ data for every engine window """
    size: Engine.math.vec2 = field(default_factory=lambda: Engine.math.vec2(Engine.data.WinDefault.size))
    title: str = field(default_factory=lambda: Engine.data.WinDefault.title)
    monitor: int | None = field(default_factory=lambda: Engine.data.WinDefault.monitor)
    vsync: int = field(default_factory=lambda: Engine.data.WinDefault.vsync)
    full: bool = field(default_factory=lambda: Engine.data.WinDefault.full)
    is_desktop: bool = field(default_factory=lambda: Engine.data.WinDefault.is_desktop)
    is_desktop_size: bool = field(default_factory=lambda: Engine.data.WinDefault.is_desktop_size)
    flags: int = field(default_factory=lambda: Engine.data.WinDefault.flags)

    def to_kwargs(self):
        kwargs = {
            'size': self.size,
            'flags': self.flags,
            'vsync': self.vsync,
        }
        if self.monitor is not None:
            kwargs['display'] = self.monitor
        return kwargs
