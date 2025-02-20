from typing import Optional

import Engine
from Engine.objects.object_node.object_node import ObjectNode

from Engine.objects.ieventful import IEventful
from Engine.objects.iupdatable import IPreUpdatable, IUpdatable
from Engine.objects.irenderable import IPreRenderable, IRenderable


class Object(ObjectNode, IEventful, IPreUpdatable, IUpdatable, IPreRenderable, IRenderable):
    data: 'Engine.objects.ObjectData'
    # ObjectData
    priority: int
    model: Optional[str]

    def __init__(self, data: 'Engine.objects.ObjectData'):
        super().__init__(data)
