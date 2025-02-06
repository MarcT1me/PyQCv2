from dataclasses import dataclass, field

import Engine.data
from Engine.objects.scene.scene_object_data import SceneObjectData
from Engine.math import vec2


@dataclass(init=True)
class CameraData(SceneObjectData):
    camera_type: str = "perspective"
    fov: int = 75
    post_process: list[str] = field(default_factory=list)
    clip_planes: vec2 = field(default_factory=lambda: vec2(
        Engine.graphic.System.gl_data.near, Engine.graphic.System.gl_data.far
    ))
