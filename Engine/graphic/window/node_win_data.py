from typing_extensions import deprecated
from dataclasses import dataclass, field

import Engine
from Engine.graphic.window import WinData


@deprecated("in a long development")
@dataclass(kw_only=True)
class NodeWinData(WinData):
    pos: Engine.math.vec2 | None = field(default=None)
    opacity: float = field(default=1.0)
    relative_mouse: bool = field(default=False)
    is_desktop: bool = field(default=True)
