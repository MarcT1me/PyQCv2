from dataclasses import dataclass
from Engine.objects.metadata import MetaData
from Engine.math import vec3


@dataclass(init=True)
class ObjectData(MetaData):
    is_active: bool = True
    position: vec3 = vec3(0)
    direction: vec3 = vec3(0)
    scale: vec3 = vec3(1)
