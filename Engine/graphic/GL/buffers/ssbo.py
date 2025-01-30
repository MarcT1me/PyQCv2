from typing import Iterable

import Engine
from Engine.graphic.GL.buffers.buffer import Buffer
from Engine.graphic.GL.buffers.buffer_object_data import BufferObjectData


class SSBO(Buffer):
    def __init__(self, data: Iterable[Engine.T], metadata: BufferObjectData):
        metadata.dynamic = True
        super().__init__(data, metadata)
        self._buffer.bind_to_storage_buffer(metadata.binding, metadata.offset, metadata.size)
