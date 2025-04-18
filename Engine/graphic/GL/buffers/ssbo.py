import Engine
from Engine.graphic.GL.buffers.buffer import Buffer


class SSBO(Buffer):
    def __init__(self, data: 'Engine.graphic.GL.BufferData'):
        super().__init__(data)

    def bind_to_shader(self, shader_id: Engine.data.Identifier):
        super().bind_to_shader(shader_id)
        self._buffer.bind_to_storage_buffer(self.data.binding, self.data.offset, self.data.size)
