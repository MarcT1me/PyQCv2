from dataclasses import dataclass, field

import Engine


@dataclass(kw_only=True)
class WinData(Engine.data.MetaData):
    """ data for every engine window """
    size: Engine.math.ivec2 = field(default_factory=lambda: Engine.math.ivec2(Engine.data.WinDefault.size))
    title: str = field(default_factory=lambda: Engine.data.WinDefault.title)
    # ico_path: str = field(default_factory=lambda: Engine.data.FileSystem.APPLICATION_ICO_asset_path)
    monitor: int | None = field(default_factory=lambda: Engine.data.WinDefault.monitor)

    vsync: int = field(default_factory=lambda: Engine.data.WinDefault.vsync)

    full: bool = field(default_factory=lambda: Engine.data.WinDefault.full)
    frameless: bool = field(default_factory=lambda: Engine.data.WinDefault.frameless)

    flags: int = field(default_factory=lambda: Engine.data.WinDefault.flags)

    def __post_init__(self):
        self.size = Engine.math.ivec2(self.size)

    def to_kwargs(self):
        kwargs = {
            "size": self.size,
            "flags": self.flags,
            "vsync": self.vsync,
        }
        if self.monitor is not False:
            kwargs["display"] = self.monitor
        return kwargs
