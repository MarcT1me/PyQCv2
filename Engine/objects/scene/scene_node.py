from abc import abstractmethod
from typing import Optional, Self

import Engine
from Engine.objects.object.object import Object


class SceneNode(Object):
    data: 'Engine.objects.SceneNodeData'
    # SceneNodeData
    scene_id: str
    parent_id: Optional[str]
    children_ids: dict[str, Self]

    def __init__(self, data: 'Engine.objects.SceneNodeData'):
        super().__init__(data)

    @abstractmethod
    def event(self, event: Engine.events.Event):
        ...

    @abstractmethod
    def update(self):
        ...
