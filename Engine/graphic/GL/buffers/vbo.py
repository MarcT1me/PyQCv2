import Engine
from Engine.graphic.GL.buffers.buffer import Buffer


class VBO(Buffer):
    def __init__(self, data: 'Engine.graphic.GL.BufferData'):
        super().__init__(data)


