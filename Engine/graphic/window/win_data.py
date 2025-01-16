from dataclasses import dataclass, field
from Engine.objects import MetaDate
from Engine.math import vec2
from Engine.data.config import Win


@dataclass
class WinData(MetaDate):
    id: str = "Main"
    """ data for every engine window """
    size: vec2 = field(default_factory=lambda: Win.size)
    monitor: int | None = field(default_factory=lambda: Win.monitor)
    title: str = field(default_factory=lambda: Win.title)
    vsync: int = field(default_factory=lambda: Win.vsync)
    full: bool = field(default_factory=lambda: Win.full)
    is_desktop: bool = field(default_factory=lambda: Win.is_desktop)
    flags: int = field(default_factory=lambda: Win.flags)
