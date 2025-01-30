from Engine.graphic import Graphics
from Engine.math import vec2


class Renderer:
    def __init__(self, size: vec2) -> None:
        self.texture = Graphics.context.texture(size, 4)
