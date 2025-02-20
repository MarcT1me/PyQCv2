from dataclasses import dataclass

import Engine


@dataclass(kw_only=True)
class Transform:
    position: Engine.math.vec3
    direction: Engine.math.vec3
    scale: Engine.math.vec3
