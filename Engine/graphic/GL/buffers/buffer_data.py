from typing import Any
from dataclasses import dataclass, field

import Engine
from Engine.graphic.GL.gl_object import GlObjectData


@dataclass(kw_only=True)
class BufferData(GlObjectData):
    dynamic: bool = field(default=False)
    array: list[Engine.T] = field(default_factory=list)
    layout: Any = field(default=None)
    offset: int = field(default=0)

    @property
    def size(self) -> int:
        return len(self.array)
