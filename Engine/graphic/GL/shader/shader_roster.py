import Engine


class ShadersRoster(Engine.data.arrays.SimpleRoster):
    def add(self, shader: 'Engine.graphic.GL.Shader'):
        shader.is_in_roster = True
        self[shader.id] = shader

    def remove(self, identifier: Engine.data.Identifier):
        self.pop(identifier).is_in_roster = False

    def __release__(self):
        for shader in self.values():
            shader.__release__()

    def clear(self):
        self.__release__()
        super().clear()
