from dataclasses import dataclass, field

import Engine.data
from Engine.objects.scene.scene_node_data import SceneNodeData
from Engine.math import vec2


@dataclass(init=True)
class CameraData(SceneNodeData):
    camera_type: str = "perspective"
    fov: int = 75
    post_process: list[str] = field(default_factory=list)
    clip_planes: vec2 = field(default_factory=lambda: vec2(
        Engine.App.graphic.gl_data.near, Engine.app.App.graphic.gl_data.far
    ))
