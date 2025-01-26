from dataclasses import dataclass

from Engine.objects.scene.scene_object_data import SceneObjectData
from Engine.math import vec3


@dataclass
class LightData(SceneObjectData):
    light_data: str = "simple"
    color: vec3 = vec3(1, 1, 1)
    intensity: float = 1


@dataclass
class PointLightData(LightData):
    light_data: str = "point"
    radius: int = 10


@dataclass
class DirectionalLightData(LightData):
    light_data: str = "directional"
    ...


@dataclass
class SpotLightData(PointLightData):
    light_data: str = "spot"
    ...
