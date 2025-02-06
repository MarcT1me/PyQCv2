from Engine.graphic import System
from Engine.math import vec2


class Renderer:
    def __init__(self, size: vec2) -> None:
        self.texture = System.context.texture(size, 4)
