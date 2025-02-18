from dataclasses import dataclass

from Engine.objects.object_node.object_node_data import ObjectNodeData
from Engine.math import vec3


@dataclass
class SimpleLightData(ObjectNodeData):
    color: vec3 = vec3(1, 1, 1)
    intensity: float = 1


@dataclass
class PointLightData(SimpleLightData):
    radius: int = 10


@dataclass
class DirectionalLightData(SimpleLightData):
    # rot: vec3
    ...


@dataclass
class SpotLightData(PointLightData):
    # rot: vec3
    ...
