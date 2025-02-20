from typing import Any

import Engine
from Engine.graphic.GL.gl_object import GlObject
from Engine.graphic.GL.buffers.buffer_data import BufferData


class GLBufferError(Exception): pass


class GLBufferWriteError(GLBufferError): pass


class GLBufferBindingError(GLBufferError): pass


class Buffer(GlObject):
    data: BufferData
    # BufferData
    dynamic: bool
    array: list[Engine.T]
    layout: Any
    offset: int
    size: int

    def __init__(self, data: BufferData):
        super().__init__(data)
        try:
            self._buffer: Engine.mgl.Buffer = Engine.App.graphic.context.buffer(
                self.array,
                dynamic=data.dynamic)
        except Exception as e:
            raise GLBufferError(f"failed to init buffer {data.id}") from e

    def bind_to_shader(self, shader_id: Engine.data.Identifier):
        try:
            Engine.App.graphic.shader_roster[shader_id][self.id.name] = self.binding
        except Exception as e:
            raise GLBufferBindingError(f"Cant bind buffer {self.id} to shader {shader_id}") from e

    def bind(self, *attributes: list[Any]):
        try:
            self._buffer.bind(*attributes, self.layout)
        except Exception as e:
            raise GLBufferBindingError(f"Cant bind buffer {self.id}") from e

    def __setitem__(self, index: int, value: list[Engine.T]):
        if index < 0 or index >= len(self.array):
            raise IndexError("Invalid index for buffer.")
        self.array[index:] = value[:]

    def __getitem__(self, index: int):
        return self.array[index]

    @property
    def default_segment(self) -> tuple[int, int]:
        return 0, len(self.array)

    def change(self, segment: tuple[int, int] = None):
        try:
            self._buffer.write(self.array[segment[0]:segment[1]], offset=segment[0])
        except Exception as e:
            raise GLBufferWriteError(f"failed to change data segment {segment}") from e

    def transfer_data(self) -> None:
        try:
            self._buffer.write(self.array)
        except Exception as e:
            raise GLBufferWriteError(f"failed to transfer data") from e
