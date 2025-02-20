from dataclasses import dataclass

import Engine


@dataclass(kw_only=True)
class VertexAttributes:
    vertices: Engine.math.vec3
    normals: Engine.math.vec3
