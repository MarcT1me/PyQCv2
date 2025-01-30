from dataclasses import dataclass

from Engine.graphic.GL.buffers.buffer_data import BufferData


@dataclass(init=True)
class BufferObjectData(BufferData):
    offset: int = 0
    size: int = -1
