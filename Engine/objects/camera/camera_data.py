from dataclasses import dataclass, field

import Engine.data
from Engine.objects.object_node.object_node_data import ObjectNodeData
from Engine.math import vec2


@dataclass(kw_only=True)
class CameraData(ObjectNodeData):
    camera_type: 'Engine.objects.CameraTypes' = None
    fov: int = None
    post_process: list[str] = field(default_factory=list)
    clip_planes: vec2 = field(default_factory=lambda: vec2(
        Engine.App.graphic.gl_data.near, Engine.app.App.graphic.gl_data.far
    ))
