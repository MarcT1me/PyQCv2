from dataclasses import dataclass, field
from Engine.objects.metadate import MetaDate
from Engine.math import vec3


@dataclass
class ObjectDate(MetaDate):
    position: vec3 = field(default=vec3(0))
    direction: vec3 = field(default=vec3(0))
    scale: vec3 = field(default=vec3(0))
