from dataclasses import dataclass

from Engine.graphic.GL.GlObject import GlObjectData


@dataclass(init=True)
class BufferData(GlObjectData):
    dynamic: bool = False
