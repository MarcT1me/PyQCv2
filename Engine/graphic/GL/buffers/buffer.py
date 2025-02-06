from typing import Iterable, Any

import Engine
from Engine.graphic.GL.GlObject import GlObject
from Engine.graphic.GL.buffers.buffer_data import BufferData


class Buffer(GlObject):
    def __init__(self, data: Iterable[Engine.T], metadata: BufferData):
        super().__init__(metadata)
        self.data = data
        self._buffer: Engine.mgl.Buffer = Engine.graphic.System.context.buffer(
            data,
            dynamic=metadata.dynamic)

    def bind(self, *attributes: Iterable[Any], layout: Any = None):
        self._buffer.bind(*attributes, layout)

    def __setitem__(self, key: int, value: Iterable[Engine.T], change=True):
        if key < 0 or key >= len(self.metadata.data):
            raise IndexError("Invalid index for buffer.")
        self.data[key:] = value[:]
        self.change(segment=(key, len(value))) if change else Ellipsis

    def __getitem__(self, item: Engine.T):
        return self.data

    def change(self, segment: tuple[int, int]):
        self._buffer.write(self.data[segment[0]:segment[1]], offset=segment[0])

    def transfer_data(self) -> None:
        self._buffer.write(self.data)
