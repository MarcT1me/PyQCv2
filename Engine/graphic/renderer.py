import Engine
from Engine.math import vec2


class Renderer:
    def __init__(self, size: vec2) -> None:
        self.texture = Engine.App.graphic.context.texture(size, 4)

    def prepare(self):
        pass

    def render(self):
        pass
