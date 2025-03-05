import Engine
from Engine.objects.scene_node.scene_node import SceneNode


class ObjectNode(SceneNode):
    data: 'Engine.objects.ObjectNodeData'
    # ObjectDdata
    transform: 'Engine.data.Transform'
    status: 'Engine.objects.ObjectStatusFlags'

    def __init__(self, data: 'Engine.objects.ObjectNodeData'):
        super().__init__(data)

    def is_pre_renderable(self) -> bool:
        return super().is_pre_renderable() and self.data.status.is_renderable

    def is_renderable(self) -> bool:
        return super().is_renderable() and self.data.status.is_renderable and self.data.status.is_visible
