import Engine


class GlObject(Engine.data.MetaObject):
    data: 'Engine.graphic.GL.GlObjectData'
    # GlObjectData
    binding: int

    def __init__(self, metadata: 'Engine.graphic.GL.GlObjectData'):
        super().__init__(metadata)
