from dataclasses import dataclass, field
from Engine.objects import MetaDate
from Engine.math import vec2
from Engine.data.config import Win


@dataclass
class WinData(MetaDate):
    id: str = "Main"
    """ data for every engine window """
    size: vec2 = field(default_factory=lambda: Win.DEFAULT_WIN_SIZE)
    monitor: int | None = field(default_factory=lambda: Win.DEFAULT_WIN_MONITOR)
    title: str = field(default_factory=lambda: Win.DEFAULT_WIN_TITLE)
    vsync: int = field(default_factory=lambda: Win.DEFAULT_WIN_VSYNC)
    flags: int = field(default_factory=lambda: Win.DEFAULT_WIN_FLAGS)
