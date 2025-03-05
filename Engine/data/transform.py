from dataclasses import dataclass, field

import Engine


@dataclass
class Transform:
    position: Engine.math.vec_type = field(default=None)
    direction: Engine.math.vec_type = field(default=None)
    scale: Engine.math.vec_type = field(default=None)

    def move(self, position: Engine.math.vec_type):
        self.position += position

    def rotate(self, rotation: Engine.math.vec_type):
        self.direction += rotation

    def zoom(self, scale: Engine.math.vec_type):
        self.scale += scale
