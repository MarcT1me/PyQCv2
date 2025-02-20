from dataclasses import dataclass

from Engine.objects.object_node.object_node_data import ObjectNodeData
from Engine.math import vec3


@dataclass(kw_only=True)
class SimpleLightData(ObjectNodeData):
    color: vec3 = vec3(1, 1, 1)
    intensity: float = 1


@dataclass(kw_only=True)
class PointLightData(SimpleLightData):
    radius: int = 10


@dataclass(kw_only=True)
class DirectionalLightData(SimpleLightData):
    # rot: vec3
    ...


@dataclass(kw_only=True)
class SpotLightData(PointLightData):
    # rot: vec3
    ...
