from typing import Optional

import Engine
from Engine.objects.object_node.object_node import ObjectNode

from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IUpdatable
from Engine.objects.irenderable import IPreRenderable


class Light(ObjectNode, IEventful, IUpdatable, IPreRenderable):
    data: 'Engine.objects.SimpleLightData'
    # LightData
    color: Engine.math.vec3
    intensity: float = 1
    # for the Point light type
    radius: Optional[int]

    def __init__(self, data: 'Engine.objects.SimpleLightData'):
        super().__init__(data)
