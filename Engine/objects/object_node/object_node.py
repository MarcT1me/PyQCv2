from abc import abstractmethod

import Engine
from Engine.objects.scene_node.scene_node import SceneNode


class ObjectNode(SceneNode):
    data: 'Engine.objects.ObjectNodeData'
    # ObjectDdata
    transform: 'Engine.data.Transform'
    flags: 'Engine.objects.ObjectFlags'

    @abstractmethod
    def __init__(self, data: 'Engine.objects.ObjectNodeData'):
        super().__init__(data)
