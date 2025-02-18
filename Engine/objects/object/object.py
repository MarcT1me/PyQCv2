from abc import abstractmethod
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

    @abstractmethod
    def __init__(self, data: 'Engine.objects.ObjectData'):
        super().__init__(data)

    @abstractmethod
    @Engine.decorators.single_event(virtual=True)
    def event(self, event: Engine.pg.event.Event):
        pass

    @abstractmethod
    def pre_update(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def pre_render(self):
        pass

    @abstractmethod
    def render(self):
        pass
