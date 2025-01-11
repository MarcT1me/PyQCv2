from dataclasses import dataclass, field
from Engine.graphic.window import WinData
from Engine.math import vec2


@dataclass
class NodeWinData(WinData):
    pos: vec2 | None = field(default=None)
    opacity: float = field(default=1.0)
    relative_mouse: bool = field(default=False)
    is_desktop: bool = field(default=True)
